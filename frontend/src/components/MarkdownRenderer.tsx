import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface MarkdownRendererProps {
    content: string;
}

const CodeBlock = ({ inline, className, children, ...props }: any) => {
    const [isCopied, setIsCopied] = useState(false);
    const match = /language-(\w+)/.exec(className || '');
    const codeString = String(children).replace(/\n$/, '');

    const handleCopy = () => {
        navigator.clipboard.writeText(codeString);
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
    };

    return !inline && match ? (
        <div className="relative rounded-md overflow-hidden my-4 border border-border/40">
            <div className="bg-muted px-4 py-2 text-xs text-muted-foreground flex justify-between items-center bg-zinc-900 border-b border-white/5">
                <span className="font-mono font-medium text-zinc-400">{match[1]}</span>
                <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 text-zinc-400 hover:text-white hover:bg-white/10"
                    onClick={handleCopy}
                >
                    {isCopied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                </Button>
            </div>
            <SyntaxHighlighter
                style={vscDarkPlus}
                language={match[1]}
                PreTag="div"
                customStyle={{ margin: 0, borderRadius: '0 0 0.375rem 0.375rem', fontSize: '0.875rem' }}
                {...props}
            >
                {codeString}
            </SyntaxHighlighter>
        </div>
    ) : (
        <code className={cn("bg-muted px-1.5 py-0.5 rounded text-sm font-mono text-rose-500 bg-rose-500/10", className)} {...props}>
            {children}
        </code>
    );
};

const MarkdownRenderer = ({ content }: MarkdownRendererProps) => {
    return (
        <div className="markdown-body space-y-3 prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:p-0 prose-pre:bg-transparent">
            <ReactMarkdown
                // remarkMath with singleDollarTextMath:false → only $$…$$ renders as math, so
                // currency like "₹1 = $0.012 and €1 = $1.08" is never mis-parsed as a formula.
                remarkPlugins={[remarkGfm, [remarkMath, { singleDollarTextMath: false }]]}
                rehypePlugins={[rehypeKatex]}
                components={{
                    code: CodeBlock,
                    p: ({ children }) => <p className="mb-3 leading-relaxed last:mb-0">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc ml-6 mb-4 space-y-1 marker:text-muted-foreground">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal ml-6 mb-4 space-y-1 marker:text-muted-foreground">{children}</ol>,
                    li: ({ children }) => <li className="pl-1">{children}</li>,
                    h1: ({ children }) => <h1 className="text-2xl font-bold mb-4 mt-6 border-b pb-2 tracking-tight">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-xl font-bold mb-3 mt-5 tracking-tight">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-lg font-bold mb-2 mt-4 tracking-tight">{children}</h3>,
                    blockquote: ({ children }) => (
                        <blockquote className="border-l-4 border-primary/30 pl-4 py-2 my-4 italic text-muted-foreground bg-muted/30 rounded-r-lg">
                            {children}
                        </blockquote>
                    ),
                    table: ({ children }) => (
                        <div className="overflow-x-auto my-6 border border-border rounded-lg shadow-sm">
                            <table className="min-w-full divide-y divide-border text-sm">
                                {children}
                            </table>
                        </div>
                    ),
                    thead: ({ children }) => <thead className="bg-muted/50 font-medium">{children}</thead>,
                    tbody: ({ children }) => <tbody className="divide-y divide-border bg-card/50">{children}</tbody>,
                    tr: ({ children }) => <tr className="divide-x divide-border transition-colors hover:bg-muted/30">{children}</tr>,
                    th: ({ children }) => <th className="px-4 py-3 text-left font-semibold text-muted-foreground tracking-wide border-b border-border">{children}</th>,
                    td: ({ children }) => <td className="px-4 py-3 whitespace-pre-wrap">{children}</td>,
                    a: ({ href, children }) => (
                        <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline font-medium decoration-blue-500/30 underline-offset-4">
                            {children}
                        </a>
                    ),
                    hr: () => <hr className="my-6 border-border" />,
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
};

export default MarkdownRenderer;
