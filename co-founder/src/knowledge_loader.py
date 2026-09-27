import os
import re
from pathlib import Path
from typing import List, Dict, Any

class KnowledgeBaseLoader:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.documents: List[Dict[str, Any]] = []
        self._load_all_documents()

    def _load_all_documents(self):
        target_dirs = ["docs", "portfolio", "knowledge-base", "templates", "memory"]
        for target in target_dirs:
            dir_path = self.root_dir / target
            if not dir_path.exists():
                continue
            for file_path in dir_path.glob("**/*.md"):
                try:
                    content = file_path.read_text(encoding="utf-8")
                    title = file_path.name
                    # Extract H1 if present
                    h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                    if h1_match:
                        title = h1_match.group(1).strip()
                    
                    self.documents.append({
                        "file_name": file_path.name,
                        "relative_path": str(file_path.relative_to(self.root_dir)),
                        "category": target,
                        "title": title,
                        "content": content,
                        "tokens": set(re.findall(r"\w+", content.lower()))
                    })
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")

        # Also load README.md
        readme_path = self.root_dir / "README.md"
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")
            self.documents.append({
                "file_name": "README.md",
                "relative_path": "README.md",
                "category": "root",
                "title": "Mugil Soft Solutions Overview",
                "content": content,
                "tokens": set(re.findall(r"\w+", content.lower()))
            })

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search documents based on term overlap score."""
        query_tokens = set(re.findall(r"\w+", query.lower()))
        if not query_tokens:
            return self.documents[:top_k]

        scored_docs = []
        for doc in self.documents:
            overlap = len(query_tokens.intersection(doc["tokens"]))
            if overlap > 0:
                scored_docs.append((overlap, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        results = [doc for _, doc in scored_docs[:top_k]]
        
        # If no query match, return top category matches or defaults
        if not results:
            results = self.documents[:top_k]
        return results

    def get_summary_stats(self) -> Dict[str, int]:
        stats = {}
        for doc in self.documents:
            cat = doc["category"]
            stats[cat] = stats.get(cat, 0) + 1
        return stats
