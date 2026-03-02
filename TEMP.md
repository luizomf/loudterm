I replaced my agents markdown memory with a semantic graph.

Why flat files are a dead end for agent memory and what happens when you use a DAG instead I have been building with AI agents since mid-2025. First with LangChain, then briefly with AutoGen, and for the last couple months with OpenClaw. And the whole time there was something bugging me that I could not quite articulate until I saw it break in production.

The memory problem.

The thing nobody talks about Every agent framework I have used stores memory the same way: text files. Markdown, YAML, JSON, whatever. It is all the same idea -- dump what the agent "knows" into a flat file and hope for the best.