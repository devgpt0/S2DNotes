"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { z } from "zod";

import {
  citationSchema,
  codeReviewResponseSchema,
  providerCatalogResponseSchema,
  providerIdSchema,
  ragBackendSchema,
  ragIndexResponseSchema,
  tutorGenerationResponseSchema,
  tutorGradeResponseSchema,
  type Citation,
  type CodeReviewResponse,
  type LearningTreeNode,
  type ProviderCatalogResponse,
  type ProviderId,
  type RagBackend,
  type TutorQuestion,
} from "@/lib/contracts";

import { CodingEditor, type CodeReviewInput } from "@/components/coding-editor";

type WorkspaceTab = "learn" | "tutor" | "code";
type TutorMode = "short-answer" | "multiple-choice";

interface ChatMessage {
  id: string;
  role: "assistant" | "learner";
  content: string;
  citations: Citation[];
}

interface Assessment {
  questions: TutorQuestion[];
  citations: Citation[];
  currentIndex: number;
  feedback: Record<string, { feedback: string; rating: number }>;
}

const apiErrorSchema = z.object({ error: z.string().min(1) }).strict();
const chatStreamSourcesSchema = z
  .object({ citations: z.array(citationSchema) })
  .strict();
const chatStreamTokenSchema = z.object({ token: z.string().min(1) }).strict();
const chatStreamCompleteSchema = z
  .object({ interactionId: z.string().uuid() })
  .strict();
const chatStreamErrorSchema = z.object({ error: z.string().min(1) }).strict();

const workspaceTabs: Array<{
  id: WorkspaceTab;
  label: string;
  detail: string;
}> = [
  { id: "learn", label: "Learn", detail: "Ask grounded questions" },
  { id: "tutor", label: "Tutor", detail: "Practise five questions" },
  { id: "code", label: "Code review", detail: "Improve an implementation" },
];

function userFacingError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }

  return "Something unexpected interrupted this request.";
}

async function requestApi<T>(
  endpoint: string,
  method: "GET" | "POST",
  schema: z.ZodType<T>,
  body?: unknown,
): Promise<T> {
  const response = await fetch(
    endpoint,
    body === undefined
      ? { method }
      : {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        },
  );
  let payload: unknown;
  try {
    payload = await response.json();
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error("The server returned an invalid response.");
    }

    throw error;
  }

  if (!response.ok) {
    const errorResult = apiErrorSchema.safeParse(payload);
    throw new Error(
      errorResult.success
        ? errorResult.data.error
        : "The server could not complete this request.",
    );
  }

  const result = schema.safeParse(payload);
  if (!result.success) {
    throw new Error("The server returned a response with an invalid schema.");
  }

  return result.data;
}

function topicForFile(path: string): string {
  const segment = path.split("/")[0];
  return segment && segment.length > 0 ? segment : "General";
}

function CitationCards({ citations }: { citations: Citation[] }) {
  if (citations.length === 0) {
    return null;
  }

  return (
    <section className="citation-list" aria-label="Retrieved sources">
      <p className="citation-title">Grounded in</p>
      {citations.map((citation) => (
        <article
          className="citation-card"
          key={citation.path + citation.heading}
        >
          <div>
            <strong>{citation.heading}</strong>
            <span>{citation.path}</span>
          </div>
          <span className="score">{citation.score.toFixed(3)}</span>
          <p>{citation.snippet}</p>
        </article>
      ))}
    </section>
  );
}

function LearningFileTree({
  nodes,
  selectedFiles,
  onFilesChange,
  disabled,
  depth = 0,
}: {
  nodes: LearningTreeNode[];
  selectedFiles: string[];
  onFilesChange: (files: string[]) => void;
  disabled: boolean;
  depth?: number;
}) {
  const selectedFileSet = new Set(selectedFiles);

  function toggleFile(path: string, selected: boolean): void {
    if (selected) {
      if (selectedFiles.length >= 20) {
        return;
      }
      onFilesChange([...selectedFiles, path]);
      return;
    }

    onFilesChange(selectedFiles.filter((file) => file !== path));
  }

  return (
    <ul className="learning-tree">
      {nodes.map((node) => {
        if (node.children.length > 0) {
          return (
            <li key={node.path}>
              <details open={depth === 0}>
                <summary>{node.name}</summary>
                <LearningFileTree
                  nodes={node.children}
                  selectedFiles={selectedFiles}
                  onFilesChange={onFilesChange}
                  disabled={disabled}
                  depth={depth + 1}
                />
              </details>
            </li>
          );
        }

        const isSelected = selectedFileSet.has(node.path);
        return (
          <li key={node.path}>
            <label className="tree-file">
              <input
                type="checkbox"
                checked={isSelected}
                disabled={
                  disabled || (!isSelected && selectedFiles.length >= 20)
                }
                onChange={(event) =>
                  toggleFile(node.path, event.target.checked)
                }
              />
              <span>{node.name}</span>
            </label>
          </li>
        );
      })}
    </ul>
  );
}

function SourcePanel({
  catalog,
  provider,
  useRag,
  ragBackend,
  selectedTopic,
  selectedFiles,
  isIndexing,
  onProviderChange,
  onRagChange,
  onRagBackendChange,
  onTopicChange,
  onFilesChange,
  onIndex,
}: {
  catalog: ProviderCatalogResponse | null;
  provider: ProviderId;
  useRag: boolean;
  ragBackend: RagBackend;
  selectedTopic: string;
  selectedFiles: string[];
  isIndexing: boolean;
  onProviderChange: (provider: ProviderId) => void;
  onRagChange: (enabled: boolean) => void;
  onRagBackendChange: (backend: RagBackend) => void;
  onTopicChange: (topic: string) => void;
  onFilesChange: (files: string[]) => void;
  onIndex: () => Promise<void>;
}) {
  const files = catalog?.rag.files ?? [];
  const topics = Array.from(new Set(files.map(topicForFile))).sort();
  return (
    <aside className="source-panel" aria-label="Learning context">
      <div className="panel-heading">
        <p className="eyebrow">Workspace context</p>
        <h2>Set the frame</h2>
      </div>

      <label className="field">
        <span>Provider</span>
        <select
          value={provider}
          onChange={(event) => {
            const providerResult = providerIdSchema.safeParse(
              event.target.value,
            );
            if (!providerResult.success) {
              throw new Error("The selected provider is invalid.");
            }

            onProviderChange(providerResult.data);
          }}
          disabled={!catalog}
        >
          {catalog?.providers.map((item) => (
            <option key={item.id} value={item.id}>
              {item.label} · {item.configured ? item.model : "not configured"}
            </option>
          ))}
        </select>
      </label>

      <div className="provider-state">
        <span
          className={
            catalog?.providers.find((item) => item.id === provider)?.configured
              ? "status-dot online"
              : "status-dot"
          }
        >
          <span />
        </span>
        <p>
          {catalog?.providers.find((item) => item.id === provider)?.configured
            ? "Credentials stay on the server."
            : "Add a server-side provider key to begin."}
        </p>
      </div>

      <div className="rag-control">
        <div>
          <span>RAG context</span>
          <p>
            {catalog?.rag.available
              ? "Retrieve relevant learning notes."
              : (catalog?.rag.message ?? "Checking retrieval service…")}
          </p>
        </div>
        <button
          className={"toggle" + (useRag ? " active" : "")}
          type="button"
          role="switch"
          aria-checked={useRag}
          disabled={!catalog?.rag.available}
          onClick={() => onRagChange(!useRag)}
        >
          <span />
        </button>
      </div>

      <label className="field">
        <span>RAG backend</span>
        <select
          value={ragBackend}
          disabled={!useRag || !catalog?.rag.available}
          onChange={(event) => {
            const backendResult = ragBackendSchema.safeParse(
              event.target.value,
            );
            if (!backendResult.success) {
              throw new Error("The selected RAG backend is invalid.");
            }

            onRagBackendChange(backendResult.data);
          }}
        >
          <option value="local">Local index</option>
          <option value="upstash" disabled={!catalog?.rag.upstashAvailable}>
            {catalog?.rag.upstashAvailable
              ? "Upstash Vector"
              : "Upstash Vector (not configured or indexed)"}
          </option>
        </select>
      </label>

      <button
        className="quiet-button"
        type="button"
        disabled={isIndexing}
        onClick={() => void onIndex()}
      >
        {isIndexing ? "Indexing learning corpus…" : "Index learning corpus"}
      </button>

      <label className="field">
        <span>Topic</span>
        <select
          value={selectedTopic}
          disabled={files.length === 0}
          onChange={(event) => onTopicChange(event.target.value)}
        >
          <option value="all">All learning topics</option>
          {topics.map((topic) => (
            <option key={topic} value={topic}>
              {topic}
            </option>
          ))}
        </select>
      </label>

      <div className="field file-field">
        <span>Learning folder and file tree</span>
        <div className="tree-shell" aria-label="Learning folder and file tree">
          {catalog && catalog.rag.tree.length > 0 ? (
            <LearningFileTree
              nodes={catalog.rag.tree}
              selectedFiles={selectedFiles}
              onFilesChange={onFilesChange}
              disabled={!useRag}
            />
          ) : (
            <small>No indexable learning files are available yet.</small>
          )}
        </div>
        <small>
          {selectedFiles.length === 0
            ? "No file limit: retrieve from the corpus."
            : selectedFiles.length +
              " file" +
              (selectedFiles.length === 1 ? "" : "s") +
              " selected."}
        </small>
      </div>
    </aside>
  );
}

function LearnPanel({
  messages,
  draft,
  disabled,
  isSending,
  onDraftChange,
  onSend,
}: {
  messages: ChatMessage[];
  draft: string;
  disabled: boolean;
  isSending: boolean;
  onDraftChange: (value: string) => void;
  onSend: () => Promise<void>;
}) {
  return (
    <section className="learn-panel" aria-labelledby="learn-heading">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Learning conversation</p>
          <h2 id="learn-heading">Turn notes into understanding</h2>
        </div>
        <span className="question-count">
          {messages.filter((message) => message.role === "learner").length}{" "}
          questions
        </span>
      </div>

      <div className="conversation" aria-live="polite">
        {messages.map((message) => (
          <article className={"message " + message.role} key={message.id}>
            <span className="message-role">
              {message.role === "assistant" ? "Genius" : "You"}
            </span>
            <p>{message.content}</p>
            <CitationCards citations={message.citations} />
          </article>
        ))}
      </div>

      <div className="composer">
        <textarea
          aria-label="Ask a learning question"
          value={draft}
          maxLength={8_000}
          onChange={(event) => onDraftChange(event.target.value)}
          placeholder="Ask about a concept, compare approaches, or request an example…"
        />
        <button
          className="primary-button"
          type="button"
          disabled={disabled || isSending || draft.length === 0}
          onClick={() => void onSend()}
        >
          {isSending ? "Thinking…" : "Ask Genius"}
        </button>
      </div>
    </section>
  );
}

function TutorPanel({
  assessment,
  tutorMode,
  topic,
  answer,
  disabled,
  isLoading,
  onModeChange,
  onTopicChange,
  onAnswerChange,
  onStart,
  onSubmitAnswer,
}: {
  assessment: Assessment | null;
  tutorMode: TutorMode;
  topic: string;
  answer: string;
  disabled: boolean;
  isLoading: boolean;
  onModeChange: (mode: TutorMode) => void;
  onTopicChange: (topic: string) => void;
  onAnswerChange: (answer: string) => void;
  onStart: () => Promise<void>;
  onSubmitAnswer: () => Promise<void>;
}) {
  const currentQuestion = assessment?.questions[assessment.currentIndex];
  const previousQuestion =
    assessment && assessment.currentIndex > 0
      ? assessment.questions[assessment.currentIndex - 1]
      : undefined;
  const latestFeedback = previousQuestion
    ? assessment?.feedback[previousQuestion.id]
    : undefined;
  const isComplete =
    assessment !== null &&
    Object.keys(assessment.feedback).length === assessment.questions.length;

  return (
    <section className="tutor-panel" aria-labelledby="tutor-heading">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Guided practice</p>
          <h2 id="tutor-heading">A five-question focused session</h2>
        </div>
        <span className="session-badge">5 questions</span>
      </div>

      <div className="tutor-setup">
        <div className="segmented-control" aria-label="Assessment mode">
          <button
            className={tutorMode === "short-answer" ? "selected" : ""}
            type="button"
            onClick={() => onModeChange("short-answer")}
          >
            Short answer
          </button>
          <button
            className={tutorMode === "multiple-choice" ? "selected" : ""}
            type="button"
            onClick={() => onModeChange("multiple-choice")}
          >
            Multiple choice
          </button>
        </div>
        <label className="topic-input">
          <span>Session topic</span>
          <input
            value={topic}
            maxLength={160}
            onChange={(event) => onTopicChange(event.target.value)}
            placeholder="For example: ownership and borrowing"
          />
        </label>
        <button
          className="primary-button"
          type="button"
          disabled={disabled || isLoading || topic.length === 0}
          onClick={() => void onStart()}
        >
          {isLoading ? "Preparing…" : "Start five questions"}
        </button>
      </div>

      {!assessment && (
        <div className="empty-state">
          <span className="empty-icon">01</span>
          <div>
            <h3>Build a small practice loop</h3>
            <p>
              Select a topic and response style. Genius will create five
              targeted questions, then coach each response.
            </p>
          </div>
        </div>
      )}

      {assessment && !isComplete && currentQuestion && (
        <div className="question-card">
          {latestFeedback && (
            <article className="inline-feedback" aria-live="polite">
              <p className="eyebrow">
                Feedback for question {assessment.currentIndex}
              </p>
              <span className="rating-badge">
                Rating {latestFeedback.rating}/5
              </span>
              <p>{latestFeedback.feedback}</p>
            </article>
          )}
          <div className="progress-copy">
            <span>
              Question {assessment.currentIndex + 1} of{" "}
              {assessment.questions.length}
            </span>
            <div className="progress-track">
              <span
                style={{
                  width:
                    ((assessment.currentIndex + 1) /
                      assessment.questions.length) *
                      100 +
                    "%",
                }}
              />
            </div>
          </div>
          <h3>{currentQuestion.prompt}</h3>

          {tutorMode === "multiple-choice" ? (
            <div className="choice-grid">
              {currentQuestion.choices.map((choice) => (
                <button
                  className={
                    "choice-button" + (answer === choice ? " selected" : "")
                  }
                  key={choice}
                  type="button"
                  onClick={() => onAnswerChange(choice)}
                >
                  {choice}
                </button>
              ))}
            </div>
          ) : (
            <textarea
              className="short-answer"
              aria-label="Your short answer"
              value={answer}
              maxLength={4_000}
              onChange={(event) => onAnswerChange(event.target.value)}
              placeholder="Explain your reasoning in your own words…"
            />
          )}

          <div className="question-actions">
            <p>Feedback arrives before the next question.</p>
            <button
              className="primary-button"
              type="button"
              disabled={disabled || isLoading || answer.length === 0}
              onClick={() => void onSubmitAnswer()}
            >
              {isLoading ? "Checking…" : "Check answer"}
            </button>
          </div>
        </div>
      )}

      {assessment && isComplete && (
        <div className="assessment-summary">
          <div>
            <span className="completion-mark">✓</span>
            <p className="eyebrow">Session complete</p>
            <h3>Review the coaching notes</h3>
          </div>
          {assessment.questions.map((question, index) => (
            <article className="feedback-card" key={question.id}>
              <span>{index + 1}</span>
              <div>
                <strong>{question.prompt}</strong>
                <p>
                  <span className="rating-badge">
                    Rating {assessment.feedback[question.id].rating}/5
                  </span>
                  {assessment.feedback[question.id].feedback}
                </p>
              </div>
            </article>
          ))}
          <CitationCards citations={assessment.citations} />
        </div>
      )}
    </section>
  );
}

function CodeReviewPanel({
  disabled,
  review,
  isReviewing,
  onReview,
}: {
  disabled: boolean;
  review: CodeReviewResponse | null;
  isReviewing: boolean;
  onReview: (input: CodeReviewInput) => Promise<void>;
}) {
  return (
    <div className="code-review-layout">
      <CodingEditor
        disabled={disabled}
        isReviewing={isReviewing}
        onReview={onReview}
      />
      {review && (
        <section className="review-result" aria-live="polite">
          <p className="eyebrow">Review notes</p>
          <h2>Clear next moves</h2>
          <span className="rating-badge">Rating {review.rating}/5</span>
          <p className="review-copy">{review.review}</p>
          <CitationCards citations={review.citations} />
        </section>
      )}
    </div>
  );
}

export function GeniusWorkspace() {
  const [catalog, setCatalog] = useState<ProviderCatalogResponse | null>(null);
  const [activeTab, setActiveTab] = useState<WorkspaceTab>("learn");
  const [provider, setProvider] = useState<ProviderId>("gemini");
  const [useRag, setUseRag] = useState(false);
  const [ragBackend, setRagBackend] = useState<RagBackend>("local");
  const [selectedTopic, setSelectedTopic] = useState("all");
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [chatDraft, setChatDraft] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Choose your learning context, then ask me to explain, compare, or practise a concept.",
      citations: [],
    },
  ]);
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [tutorMode, setTutorMode] = useState<TutorMode>("multiple-choice");
  const [tutorTopic, setTutorTopic] = useState("Learning fundamentals");
  const [tutorAnswer, setTutorAnswer] = useState("");
  const [review, setReview] = useState<CodeReviewResponse | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [isTutoring, setIsTutoring] = useState(false);
  const [isReviewing, setIsReviewing] = useState(false);
  const [isIndexing, setIsIndexing] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const loadCatalog = useCallback(async (): Promise<void> => {
    try {
      const nextCatalog = await requestApi(
        "/api/providers",
        "GET",
        providerCatalogResponseSchema,
      );
      setCatalog(nextCatalog);
      const configuredProvider = nextCatalog.providers.find(
        (item) => item.configured,
      );
      if (configuredProvider) {
        setProvider(configuredProvider.id);
      }
      if (nextCatalog.rag.available) {
        setUseRag(true);
      } else {
        setUseRag(false);
      }
    } catch (error) {
      setErrorMessage(userFacingError(error));
    }
  }, []);

  useEffect(() => {
    void loadCatalog();
  }, [loadCatalog]);

  useEffect(() => {
    setConversationId(crypto.randomUUID());
  }, []);

  useEffect(() => {
    if (selectedTopic !== "all") {
      setTutorTopic(selectedTopic);
    }
  }, [selectedTopic]);

  const configured = Boolean(
    catalog?.providers.find((item) => item.id === provider)?.configured,
  );
  const sourceSelection = useMemo(
    () => ({
      useRag,
      ragBackend,
      selectedFiles,
    }),
    [ragBackend, selectedFiles, useRag],
  );

  function handleTopicChange(topic: string): void {
    setSelectedTopic(topic);
    const visibleFiles =
      topic === "all"
        ? (catalog?.rag.files ?? [])
        : (catalog?.rag.files ?? []).filter(
            (file) => topicForFile(file) === topic,
          );
    setSelectedFiles((currentFiles) =>
      currentFiles.filter((file) => visibleFiles.includes(file)),
    );
  }

  async function indexLearningCorpus(): Promise<void> {
    setErrorMessage(null);
    setStatusMessage(null);
    setIsIndexing(true);
    try {
      const result = await requestApi(
        "/api/rag/index",
        "POST",
        ragIndexResponseSchema,
        {},
      );
      setStatusMessage(
        "Indexed " +
          result.document_count +
          " documents into " +
          result.chunk_count +
          " chunks.",
      );
      await loadCatalog();
    } catch (error) {
      setErrorMessage(userFacingError(error));
    } finally {
      setIsIndexing(false);
    }
  }

  async function sendChat(): Promise<void> {
    if (!configured || !conversationId || chatDraft.length === 0) {
      return;
    }

    const draft = chatDraft;
    const assistantMessageId = crypto.randomUUID();
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "learner",
      content: draft,
      citations: [],
    };
    setErrorMessage(null);
    setIsSending(true);
    setMessages((current) => [
      ...current,
      userMessage,
      {
        id: assistantMessageId,
        role: "assistant",
        content: "",
        citations: [],
      },
    ]);
    setChatDraft("");
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider,
          message: draft,
          conversationId,
          ...sourceSelection,
        }),
      });
      if (!response.ok) {
        let payload: unknown;
        try {
          payload = await response.json();
        } catch (error) {
          if (error instanceof SyntaxError) {
            throw new Error("The server could not start the chat stream.");
          }
          throw error;
        }
        const errorResult = apiErrorSchema.safeParse(payload);
        throw new Error(
          errorResult.success
            ? errorResult.data.error
            : "The server could not start the chat stream.",
        );
      }
      if (!response.body) {
        throw new Error("The server did not return a chat stream.");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let answer = "";
      let citations: Citation[] = [];
      const updateAssistant = (interactionId?: string): void => {
        setMessages((current) =>
          current.map((message) =>
            message.id === assistantMessageId
              ? {
                  ...message,
                  id: interactionId ?? message.id,
                  content: answer,
                  citations,
                }
              : message,
          ),
        );
      };
      const processEvent = (event: string): void => {
        const lines = event.split("\n");
        const eventName = lines
          .find((line) => line.startsWith("event:"))
          ?.slice("event:".length)
          .trim();
        const data = lines
          .filter((line) => line.startsWith("data:"))
          .map((line) => line.slice("data:".length).trimStart())
          .join("\n");
        if (!eventName || !data) {
          return;
        }

        let payload: unknown;
        try {
          payload = JSON.parse(data);
        } catch (error) {
          if (error instanceof SyntaxError) {
            throw new Error(
              "The server returned an invalid chat stream event.",
            );
          }
          throw error;
        }
        if (eventName === "sources") {
          const sources = chatStreamSourcesSchema.parse(payload);
          citations = sources.citations;
          updateAssistant();
          return;
        }
        if (eventName === "token") {
          const token = chatStreamTokenSchema.parse(payload);
          answer += token.token;
          updateAssistant();
          return;
        }
        if (eventName === "complete") {
          const complete = chatStreamCompleteSchema.parse(payload);
          updateAssistant(complete.interactionId);
          return;
        }
        if (eventName === "error") {
          const streamError = chatStreamErrorSchema.parse(payload);
          throw new Error(streamError.error);
        }
        throw new Error("The server returned an unknown chat stream event.");
      };

      while (true) {
        const result = await reader.read();
        if (result.done) {
          break;
        }
        buffer += decoder
          .decode(result.value, { stream: true })
          .replaceAll("\r\n", "\n");
        let separator = buffer.indexOf("\n\n");
        while (separator >= 0) {
          processEvent(buffer.slice(0, separator));
          buffer = buffer.slice(separator + 2);
          separator = buffer.indexOf("\n\n");
        }
      }
      buffer += decoder.decode().replaceAll("\r\n", "\n");
      if (buffer.trim()) {
        processEvent(buffer);
      }
    } catch (error) {
      setMessages((current) =>
        current.filter((message) => message.id !== assistantMessageId),
      );
      setErrorMessage(userFacingError(error));
    } finally {
      setIsSending(false);
    }
  }

  async function startTutor(): Promise<void> {
    if (!configured || tutorTopic.length === 0) {
      return;
    }

    setErrorMessage(null);
    setIsTutoring(true);
    try {
      const response = await requestApi(
        "/api/tutor",
        "POST",
        tutorGenerationResponseSchema,
        {
          action: "generate",
          provider,
          mode: tutorMode,
          topic: tutorTopic,
          ...sourceSelection,
        },
      );
      setAssessment({
        questions: response.questions,
        citations: response.citations,
        currentIndex: 0,
        feedback: {},
      });
      setTutorAnswer("");
    } catch (error) {
      setErrorMessage(userFacingError(error));
    } finally {
      setIsTutoring(false);
    }
  }

  async function submitTutorAnswer(): Promise<void> {
    const question = assessment?.questions[assessment.currentIndex];
    if (!configured || !assessment || !question || tutorAnswer.length === 0) {
      return;
    }

    setErrorMessage(null);
    setIsTutoring(true);
    try {
      const response = await requestApi(
        "/api/tutor",
        "POST",
        tutorGradeResponseSchema,
        {
          action: "grade",
          provider,
          mode: tutorMode,
          topic: tutorTopic,
          question,
          answer: tutorAnswer,
          ...sourceSelection,
        },
      );
      setAssessment((current) => {
        if (!current) {
          return current;
        }

        return {
          ...current,
          currentIndex: Math.min(
            current.currentIndex + 1,
            current.questions.length - 1,
          ),
          feedback: {
            ...current.feedback,
            [question.id]: {
              feedback: response.feedback,
              rating: response.rating,
            },
          },
        };
      });
      setTutorAnswer("");
    } catch (error) {
      setErrorMessage(userFacingError(error));
    } finally {
      setIsTutoring(false);
    }
  }

  async function reviewCode(input: CodeReviewInput): Promise<void> {
    if (!configured) {
      return;
    }

    setErrorMessage(null);
    setIsReviewing(true);
    try {
      const response = await requestApi(
        "/api/code-review",
        "POST",
        codeReviewResponseSchema,
        {
          provider,
          ...input,
          ...sourceSelection,
        },
      );
      setReview(response);
    } catch (error) {
      setErrorMessage(userFacingError(error));
    } finally {
      setIsReviewing(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/">
          <span className="brand-mark">G</span>
          <span>
            <strong>Genius</strong>
            <small>Learning workspace</small>
          </span>
        </a>
        <div className="topbar-status">
          <span
            className={
              catalog?.rag.available ? "live-pill" : "live-pill offline"
            }
          >
            <i />
            {catalog?.rag.available ? "RAG connected" : "RAG offline"}
          </span>
          <span className="date-label">Learn deliberately</span>
        </div>
      </header>

      <div className="workspace-grid">
        <SourcePanel
          catalog={catalog}
          provider={provider}
          useRag={useRag}
          ragBackend={ragBackend}
          selectedTopic={selectedTopic}
          selectedFiles={selectedFiles}
          isIndexing={isIndexing}
          onProviderChange={setProvider}
          onRagChange={setUseRag}
          onRagBackendChange={setRagBackend}
          onTopicChange={handleTopicChange}
          onFilesChange={setSelectedFiles}
          onIndex={indexLearningCorpus}
        />

        <div className="workspace-content">
          <nav className="workspace-tabs" aria-label="Workspace">
            {workspaceTabs.map((tab) => (
              <button
                className={activeTab === tab.id ? "active" : ""}
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
              >
                <strong>{tab.label}</strong>
                <span>{tab.detail}</span>
              </button>
            ))}
          </nav>

          {errorMessage && (
            <div className="notice error-notice" role="alert">
              <span>!</span>
              <p>{errorMessage}</p>
              <button type="button" onClick={() => setErrorMessage(null)}>
                Dismiss
              </button>
            </div>
          )}
          {statusMessage && (
            <div className="notice success-notice" role="status">
              <span>✓</span>
              <p>{statusMessage}</p>
              <button type="button" onClick={() => setStatusMessage(null)}>
                Dismiss
              </button>
            </div>
          )}

          {activeTab === "learn" && (
            <LearnPanel
              messages={messages}
              draft={chatDraft}
              disabled={!configured || !conversationId}
              isSending={isSending}
              onDraftChange={setChatDraft}
              onSend={sendChat}
            />
          )}
          {activeTab === "tutor" && (
            <TutorPanel
              assessment={assessment}
              tutorMode={tutorMode}
              topic={tutorTopic}
              answer={tutorAnswer}
              disabled={!configured}
              isLoading={isTutoring}
              onModeChange={setTutorMode}
              onTopicChange={setTutorTopic}
              onAnswerChange={setTutorAnswer}
              onStart={startTutor}
              onSubmitAnswer={submitTutorAnswer}
            />
          )}
          {activeTab === "code" && (
            <CodeReviewPanel
              disabled={!configured}
              review={review}
              isReviewing={isReviewing}
              onReview={reviewCode}
            />
          )}
        </div>
      </div>
    </main>
  );
}
