"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

import { codingLanguageSchema, type CodingLanguage } from "@/lib/contracts";

const MonacoEditor = dynamic(
  () => import("@monaco-editor/react").then((module) => module.default),
  {
    ssr: false,
    loading: () => <div className="editor-loading">Loading code editor…</div>,
  },
);

export interface CodeReviewInput {
  language: CodingLanguage;
  code: string;
  goal: string;
}

interface CodingEditorProps {
  disabled: boolean;
  isReviewing: boolean;
  onReview: (input: CodeReviewInput) => Promise<void>;
}

interface DsaProblem {
  id: string;
  title: string;
  difficulty: "Easy" | "Medium";
  prompt: string;
  constraints: string;
}

const dsaProblems: readonly DsaProblem[] = [
  {
    id: "two-sum",
    title: "Two Sum",
    difficulty: "Easy",
    prompt:
      "Given an integer array and a target, return the indexes of two distinct values whose sum equals the target.",
    constraints: "Aim for linear time and do not use the same value twice.",
  },
  {
    id: "valid-parentheses",
    title: "Valid Parentheses",
    difficulty: "Easy",
    prompt:
      "Given a string containing bracket characters, determine whether every opening bracket is closed in the correct order.",
    constraints: "Use a stack and handle an empty input correctly.",
  },
  {
    id: "binary-search",
    title: "Binary Search",
    difficulty: "Easy",
    prompt:
      "Given a sorted integer array and a target, return its index or -1 when it does not occur.",
    constraints:
      "Use an iterative binary search and avoid integer-overflow-prone midpoint arithmetic.",
  },
  {
    id: "longest-substring",
    title: "Longest Unique Substring",
    difficulty: "Medium",
    prompt:
      "Return the length of the longest substring that contains no repeated characters.",
    constraints: "Target linear time with a sliding window.",
  },
  {
    id: "merge-intervals",
    title: "Merge Intervals",
    difficulty: "Medium",
    prompt:
      "Merge all overlapping closed intervals and return the resulting intervals ordered by start position.",
    constraints:
      "Sort before merging and account for touching interval boundaries.",
  },
];

const templates: Record<CodingLanguage, string> = {
  cpp: [
    "#include <vector>",
    "",
    "class Solution {",
    " public:",
    "  // Implement the challenge here.",
    "};",
  ].join("\n"),
  java: [
    "final class Solution {",
    "    // Implement the challenge here.",
    "}",
  ].join("\n"),
  python: [
    "class Solution:",
    "    # Implement the challenge here.",
    "    pass",
  ].join("\n"),
  go: [
    "package main",
    "",
    "// Implement the challenge here.",
    "func solve() {",
    "}",
  ].join("\n"),
  rust: [
    "struct Solution;",
    "",
    "impl Solution {",
    "    // Implement the challenge here.",
    "}",
  ].join("\n"),
};

function challengeGoal(problem: DsaProblem): string {
  return problem.title + ". " + problem.prompt + " " + problem.constraints;
}

function nextProblem(currentId: string | null): DsaProblem {
  const candidates = dsaProblems.filter((problem) => problem.id !== currentId);
  return (
    candidates[Math.floor(Math.random() * candidates.length)] ?? dsaProblems[0]
  );
}

export function CodingEditor({
  disabled,
  isReviewing,
  onReview,
}: CodingEditorProps) {
  const [problem, setProblem] = useState<DsaProblem>(dsaProblems[0]);
  const [language, setLanguage] = useState<CodingLanguage>("cpp");
  const [code, setCode] = useState(templates.cpp);

  useEffect(() => {
    const randomProblem = nextProblem(dsaProblems[0].id);
    setProblem(randomProblem);
  }, []);

  async function submitReview(): Promise<void> {
    if (disabled || code.length === 0) {
      return;
    }

    await onReview({ language, code, goal: challengeGoal(problem) });
  }

  function selectLanguage(nextLanguage: CodingLanguage): void {
    setLanguage(nextLanguage);
    setCode(templates[nextLanguage]);
  }

  function selectNewChallenge(): void {
    const randomProblem = nextProblem(problem.id);
    setProblem(randomProblem);
    setCode(templates[language]);
  }

  return (
    <section className="coding-panel" aria-labelledby="code-review-heading">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Coding lab</p>
          <h2 id="code-review-heading">Solve a focused DSA challenge</h2>
        </div>
        <label className="select-label">
          <span>Language</span>
          <select
            aria-label="Code language"
            value={language}
            onChange={(event) => {
              const languageResult = codingLanguageSchema.safeParse(
                event.target.value,
              );
              if (!languageResult.success) {
                throw new Error("The selected code language is invalid.");
              }

              selectLanguage(languageResult.data);
            }}
          >
            <option value="cpp">C++</option>
            <option value="java">Java</option>
            <option value="python">Python</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
          </select>
        </label>
      </div>

      <article className="challenge-card">
        <div>
          <span className="challenge-difficulty">{problem.difficulty}</span>
          <h3>{problem.title}</h3>
        </div>
        <p>{problem.prompt}</p>
        <small>{problem.constraints}</small>
        <button
          className="quiet-button"
          type="button"
          disabled={isReviewing}
          onClick={selectNewChallenge}
        >
          New random challenge
        </button>
      </article>

      <div className="editor-shell">
        <MonacoEditor
          height="420px"
          language={language}
          theme="vs-dark"
          value={code}
          onChange={(value) => setCode(value ?? "")}
          options={{
            automaticLayout: true,
            fontSize: 14,
            minimap: { enabled: false },
            padding: { top: 16, bottom: 16 },
            scrollBeyondLastLine: false,
            wordWrap: "on",
          }}
        />
      </div>

      <div className="action-row">
        <p>
          Genius reviews your submission only; it never executes submitted code.
        </p>
        <button
          className="primary-button"
          type="button"
          disabled={disabled || isReviewing || code.length === 0}
          onClick={() => void submitReview()}
        >
          {isReviewing ? "Reviewing…" : "Review code"}
        </button>
      </div>
    </section>
  );
}
