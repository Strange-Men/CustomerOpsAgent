import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface SafeMarkdownProps {
  content: string;
  className?: string;
}

/**
 * Safe Markdown renderer for customer-facing answers.
 * Supports: bold, lists, line breaks. Blocks: raw HTML, scripts.
 * Designed for the dark card theme.
 */
export function SafeMarkdown({ content, className = "" }: SafeMarkdownProps) {
  return (
    <div className={`safe-markdown ${className}`}>
      <Markdown
        remarkPlugins={[remarkGfm]}
        // Disable raw HTML entirely for security
        disallowedElements={["script", "style", "iframe", "object", "embed"]}
        components={{
          // Style paragraphs for the dark theme
          p: ({ children }) => (
            <p className="mb-2 last:mb-0">{children}</p>
          ),
          // Style bold text
          strong: ({ children }) => (
            <strong className="font-semibold text-slate-100">{children}</strong>
          ),
          // Style unordered lists
          ul: ({ children }) => (
            <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>
          ),
          // Style ordered lists
          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>
          ),
          // Style list items
          li: ({ children }) => (
            <li className="text-slate-200">{children}</li>
          ),
          // Style line breaks
          br: () => <br />,
        }}
      >
        {content}
      </Markdown>
    </div>
  );
}
