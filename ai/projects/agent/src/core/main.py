from core.agent_v4 import AgentV4

BANNER = r"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                              ┃
┃   ███████╗████████╗██╗   ██╗██████╗ ██╗   ██╗                                ┃
┃   ██╔════╝╚══██╔══╝██║   ██║██╔══██╗╚██╗ ██╔╝                                ┃
┃   ███████╗   ██║   ██║   ██║██║  ██║ ╚████╔╝                                 ┃
┃   ╚════██║   ██║   ██║   ██║██║  ██║  ╚██╔╝                                  ┃
┃   ███████║   ██║   ╚██████╔╝██████╔╝   ██║                                   ┃
┃   ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝    ╚═╝                                   ┃
┃                                                                              ┃
┃                          🚀 Agent V4 🚀                                       ┃
┃                                                                              ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ SEARCH MODES                                                                 ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  1. chat      → General Agent Interaction                                    ┃
┃  2. keyword   → TF-IDF Keyword Retrieval                                     ┃
┃  3. semantic  → Embedding-Based Semantic Retrieval                           ┃
┃  4. hybrid    → TF-IDF + Embedding Search                                    ┃
┃                                                                              ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ COMMANDS                                                                     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  /mode              → Show mode selection menu                               ┃
┃  /mode 1            → Switch to Chat Mode                                    ┃
┃  /mode 2            → Switch to Keyword Mode                                 ┃
┃  /mode 3            → Switch to Semantic Mode                                ┃
┃  /mode 4            → Switch to Hybrid Mode                                  ┃
┃  /mode keyword      → TF-IDF Retrieval                                       ┃
┃  /mode semantic     → Embedding Retrieval                                    ┃
┃  /mode hybrid       → Hybrid Search                                          ┃
┃  /mode chat         → General Agent                                          ┃
┃  load <path>        → Load TXT/MD/PDF/DOCX into knowledge base               ┃
┃                                                                              ┃
┃  help               → Show available commands                                ┃
┃  exit               → Quit StudyAgent                                        ┃
┃                                                                              ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Current Capabilities                                                         ┃
┃ • TF-IDF Search  • Semantic Search  • Hybrid Search                          ┃
┃ • Tokenization   • Vocabulary Engine • Cosine Similarity                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""


def main():
    agent = AgentV4()

    print(BANNER)
    while True:
        query = input("\nYou > ").strip()

        if not query:
            continue

        if query.lower() == "exit":
            print("\nAgent > Goodbye.")
            break

        response = agent.run(query)
        print(f"\nAgent > {response}")


if __name__ == "__main__":
    main()
