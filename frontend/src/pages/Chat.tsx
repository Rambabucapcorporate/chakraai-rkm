import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
  ArrowLeft,
  Send,
  BookOpen,
  Sparkles,
  User,
  Bot,
  Volume2,
  Loader2,
  Mic,
  MicOff,
  Image as ImageIcon,
  X,
  Paperclip
} from "lucide-react";
import MarkdownRenderer from "@/components/MarkdownRenderer";
import { API_BASE_URL } from "@/lib/api";

// Add global declaration for SpeechRecognition
declare global {
  interface Window {
    webkitSpeechRecognition: any;
    SpeechRecognition: any;
  }
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  image?: string; // Base64 string for preview
  suggestedQuestions?: string[];
  addlAi?: string;
}

const Chat = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState<string[]>([]); // New state
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null); // Changed type to any to bypass TS issues with missing DOM types
  const synthesisRef = useRef<SpeechSynthesis>(window.speechSynthesis);

  // Initialize speech recognition
  useEffect(() => {
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;

      recognitionRef.current.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0].transcript)
          .join("");
        setInput(transcript);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
        // Optional: Auto-submit on recording end
        // if (input.trim()) handleSubmit();
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error("Speech recognition error", event.error);
        setIsRecording(false);
      };
    }
  }, []);

  const toggleRecording = () => {
    if (isRecording) {
      recognitionRef.current?.stop();
    } else {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.start();
          setIsRecording(true);
        } catch (error) {
          console.error("Failed to start speech recognition:", error);
        }
      } else {
        alert("Speech recognition is not supported in this browser.");
      }
    }
  };

  const speak = (text: string) => {
    if (synthesisRef.current.speaking) {
      synthesisRef.current.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    synthesisRef.current.speak(utterance);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        alert("Image size should be less than 5MB");
        return;
      }
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Get metadata from URL params
  const year = searchParams.get("year") || "";
  const branch = searchParams.get("branch") || "";
  const semester = searchParams.get("semester") || "";
  const subject = searchParams.get("subject") || "";

  const handleQuestionClick = (question: string) => {
    setInput(question);
    // Use a small timeout to ensure state update before submit
    setTimeout(() => {
      const fakeEvent = { preventDefault: () => { } } as React.FormEvent;
      handleSubmit(fakeEvent, question);
    }, 0);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e?: React.FormEvent, overrideInput?: string) => {
    e?.preventDefault();
    const queryText = overrideInput || input;
    if (!queryText.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: queryText.trim(),
      timestamp: new Date(),
      image: imagePreview || undefined, // Capture the current image preview
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setSuggestedQuestions([]); // Clear previous questions

    // Prepare assistant message ID but don't add to state yet
    const assistantMessageId = (Date.now() + 1).toString();

    // Prepare FormData
    const formData = new FormData();
    formData.append("query", userMessage.content);
    formData.append("history", JSON.stringify(messages)); // Backend expects JSON string
    formData.append("subject", subject);
    formData.append("year", year);
    formData.append("branch", branch);
    formData.append("semester", semester);
    if (selectedImage) {
      formData.append("image", selectedImage);
    }

    // Clear image selection after sending
    clearImage();

    try {
      // const response = await fetch('https://apichakra.rkmvc.ac.in/api/chat', {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        // Headers are automatically set for FormData, do NOT set Content-Type manually
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      if (!response.body) {
        throw new Error('Response body is null');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let isFirstChunk = true;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Process all complete lines
        buffer = lines.pop() || ""; // Keep the last incomplete line in buffer

        for (const line of lines) {
          if (!line.trim()) continue;

          try {
            const data = JSON.parse(line);

            if (data.token) {
              if (isFirstChunk) {
                // Initialize message on first token
                setIsLoading(false);
                const assistantMessage: Message = {
                  id: assistantMessageId,
                  role: "assistant",
                  content: data.token,
                  timestamp: new Date(),
                };
                setMessages((prev) => [...prev, assistantMessage]);
                isFirstChunk = false;
              } else {
                // Append content for subsequent tokens
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMessageId
                      ? { ...msg, content: msg.content + data.token }
                      : msg
                  )
                );
              }
            } else if (data.suggested_questions) {
              setSuggestedQuestions(data.suggested_questions);
              // Also update the specific message with suggested questions
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? { ...msg, suggestedQuestions: data.suggested_questions }
                    : msg
                )
              );
            } else if (data.addl_ai || data.AddlAI) {
              const addlAiContent = data.addl_ai || data.AddlAI;
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? { ...msg, addlAi: addlAiContent }
                    : msg
                )
              );
            }
          } catch (e) {
            console.error("Error parsing NDJSON line:", line, e);
          }
        }
      }

    } catch (error) {
      console.error('Error fetching chat response:', error);

      // If error happens before we started streaming, add error message
      setMessages((prev) => {
        const messageExists = prev.some(msg => msg.id === assistantMessageId);
        if (messageExists) {
          return prev.map((msg) =>
            msg.id === assistantMessageId
              ? { ...msg, content: msg.content + "\n\n[Error: Connection interrupted]" }
              : msg
          );
        } else {
          const errorMessage: Message = {
            id: assistantMessageId,
            role: "assistant",
            content: "Sorry, I encountered an error connecting to the knowledge base. Please ensure the backend server is running.",
            timestamp: new Date(),
          };
          return [...prev, errorMessage];
        }
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="h-screen flex flex-col bg-background font-sans">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-border/40 bg-muted/30 backdrop-blur-md shadow-sm">
        <div className="w-full flex items-center justify-between h-16 px-4 sm:px-6">
          <div className="flex items-center gap-3">
            <div className="flex-shrink-0">
              <img src="/rkm-logo.png" alt="RKM Logo" className="h-10 w-auto object-contain" />
            </div>
            <div className="bg-background/80 px-1 rounded-xl shadow-sm border border-border/50 hover:bg-background transition-colors">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate("/dashboard")}
                className="h-8 gap-2 text-muted-foreground hover:text-foreground rounded-lg px-2"
              >
                <ArrowLeft className="h-4 w-4" />
                <span className="text-sm font-medium">Back</span>
              </Button>
            </div>
            <div className="flex items-center gap-2 text-sm bg-background/50 px-3 py-1.5 rounded-lg border border-border/40 backdrop-blur-sm">
              <span className="font-medium text-muted-foreground hover:text-foreground transition-colors cursor-pointer">{branch}</span>
              <span className="text-muted-foreground/60">/</span>
              <span className="font-semibold text-foreground">{subject}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-background text-rose-600 border border-rose-100 text-xs font-semibold shadow-sm">
              <Sparkles className="h-3.5 w-3.5" />
              <span>AI Chat</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden relative flex flex-col">
        {messages.length === 0 ? (
          // Empty State - Centered Search Layout
          <div className="flex-1 flex flex-col overflow-y-auto">
            <div className="flex-1 flex flex-col items-center justify-center p-4 min-h-[500px]">
              <div className="w-full max-w-2xl mx-auto flex flex-col items-center text-center space-y-8 animate-fade-in-up">

                {/* Hero Icon & Title */}
                <div className="space-y-4 flex flex-col items-center">
                  <div className="relative">
                    <div className="h-16 w-16 bg-blue-100/50 rounded-2xl flex items-center justify-center border border-blue-200/50 shadow-sm">
                      <BookOpen className="h-8 w-8 text-blue-600" />
                    </div>
                    {/* Decorative element */}
                    <div className="absolute -bottom-1 -right-1 h-6 w-6 bg-rose-100 rounded-lg flex items-center justify-center border border-rose-200">
                      <Bot className="h-3.5 w-3.5 text-rose-500" />
                    </div>
                  </div>

                  <div className="space-y-2 max-w-lg">
                    <h1 className="text-3xl font-bold bg-clip-text text-foreground tracking-tight">
                      {subject} — AI Study Assistant
                    </h1>

                    <p className="text-muted-foreground text-lg px-4">
                      Ask to summarize key {subject} chapters, compare different numerical methods, or explain component interactions described in your documentation.
                    </p>
                  </div>
                </div>

                {/* Search Box Card */}
                <div className="w-full bg-card rounded-2xl border border-border/60 shadow-lg shadow-primary/5 p-2 transition-shadow hover:shadow-xl hover:shadow-primary/10">
                  {imagePreview && (
                    <div className="relative w-fit m-2">
                      <img src={imagePreview} alt="Preview" className="h-20 w-auto rounded-lg border border-border/50 object-cover" />
                      <button
                        onClick={clearImage}
                        className="absolute -top-1.5 -right-1.5 bg-background rounded-full p-0.5 border border-border shadow-sm hover:bg-muted"
                      >
                        <X className="h-3.5 w-3.5 text-muted-foreground" />
                      </button>
                    </div>
                  )}
                  <form onSubmit={handleSubmit} className="relative">
                    <Textarea
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder={subject ? `Ask any question on ${subject}...` : "Ask any question..."}
                      className="w-full min-h-[60px] max-h-[120px] resize-none border-0 focus-visible:ring-0 bg-transparent px-4 py-3 text-base placeholder:text-muted-foreground/60 pr-24 pl-12"
                      rows={2}
                    />
                    {/* Left Icons */}
                    <div className="absolute left-3 bottom-3 flex items-center gap-1">
                      <input
                        type="file"
                        ref={fileInputRef}
                        accept="image/*"
                        className="hidden"
                        onChange={handleImageSelect}
                      />
                      <Button
                        type="button"
                        size="icon"
                        variant="ghost"
                        onClick={() => fileInputRef.current?.click()}
                        className={`h-8 w-8 rounded-lg ${selectedImage ? 'text-primary bg-primary/10' : 'text-muted-foreground hover:text-foreground'}`}
                        title="Upload Image"
                      >
                        <ImageIcon className="h-5 w-5" />
                      </Button>
                    </div>

                    {/* Right Icons */}
                    <div className="absolute right-2 bottom-2 flex items-center gap-1">
                      <Button
                        type="button"
                        size="icon"
                        variant="ghost"
                        onClick={toggleRecording}
                        className={`h-9 w-9 rounded-lg ${isRecording ? 'text-red-500 bg-red-50' : 'text-muted-foreground hover:text-foreground'}`}
                      >
                        {isRecording ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                      </Button>
                      <Button
                        type="submit"
                        size="icon"
                        disabled={!input.trim() || isLoading}
                        className="h-9 w-9 bg-rose-500 hover:bg-rose-600 text-white rounded-lg shadow-sm transition-all"
                      >
                        <Send className="h-4 w-4" />
                      </Button>
                    </div>
                  </form>

                  {/* Quick Actions inside/below the card */}

                </div>

              </div>
            </div>

            {/* Disclaimer Footer */}
            <div className="text-center py-6 text-xs text-muted-foreground/60">
              Responses are generated using course-aligned materials. Verify results for examinations.
            </div>
          </div>
        ) : (
          // Active Chat Layout
          <>
            <div className="flex-1 overflow-y-auto scroll-smooth">
              <div className="max-w-6xl mx-auto py-8 px-4 space-y-8">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-4 ${message.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    {message.role === "assistant" && (
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center border border-blue-200">
                        <Bot className="h-5 w-5 text-blue-600" />
                      </div>
                    )}

                    <div
                      className={`max-w-[85%] rounded-2xl px-5 py-3.5 relative shadow-sm ${message.role === "user"
                        ? "bg-primary text-primary-foreground rounded-tr-sm"
                        : "bg-card border border-border/60 text-foreground rounded-tl-sm w-full"
                        }`}
                    >
                      <div className={`text-sm leading-7 ${message.role === "user" ? "text-primary-foreground" : "text-foreground"}`}>
                        {message.role === "user" ? (
                          <div className="flex flex-col gap-2">
                            {message.image && (
                              <img
                                src={message.image}
                                alt="Shared image"
                                className="max-w-full rounded-lg border border-border/20 shadow-sm"
                              />
                            )}
                            <div className="whitespace-pre-wrap">{message.content}</div>
                          </div>
                        ) : (
                          (() => {
                            // Split content to separate references and suggested questions
                            let contentToRender = message.content;

                            // 1. Extract suggested questions section (🧐 Explore Further:)
                            let suggestedSection = "";
                            if (contentToRender.includes("🧐 Explore Further:")) {
                              const parts = contentToRender.split("🧐 Explore Further:");
                              contentToRender = parts[0];
                              suggestedSection = parts[1];
                              // If there are references AFTER the suggested section, we need to handle that
                              if (suggestedSection.includes("### 📚 Reference Chunks")) {
                                const subParts = suggestedSection.split("### 📚 Reference Chunks");
                                suggestedSection = subParts[0]; // Not used if we have data.suggested_questions, but good for cleanup
                                contentToRender += "### 📚 Reference Chunks" + subParts[1];
                              }
                            }

                            // 2. Split content to separate references
                            const parts = contentToRender.split("### 📚 Reference Chunks");
                            const mainContent = parts[0];
                            // Clean up references text if it exists, otherwise empty
                            const referencesContent = parts.length > 1 ? "### 📚 Reference Chunks" + parts[1] : "";

                            return (
                              <div className="space-y-4">
                                {message.addlAi ? (
                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 split-responses animate-fade-in">
                                    {/* Primary AI Response */}
                                    <div className="space-y-2">
                                      <div className="flex items-center gap-1.5 text-xs font-bold text-primary/70 uppercase tracking-wider mb-2">
                                        <Bot className="h-3.5 w-3.5 text-blue-500" />
                                        <span>Primary AI</span>
                                      </div>
                                      <MarkdownRenderer content={mainContent} />
                                    </div>
                                    
                                    {/* Additional AI Response */}
                                    <div className="border-t md:border-t-0 md:border-l border-border/60 pt-4 md:pt-0 md:pl-6 space-y-2">
                                      <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-2">
                                        <Sparkles className="h-3.5 w-3.5 animate-pulse text-indigo-500" />
                                        <span>Additional AI</span>
                                      </div>
                                      <div className="markdown-addl-ai text-sm text-foreground/90 leading-relaxed">
                                        <MarkdownRenderer content={message.addlAi} />
                                      </div>
                                    </div>
                                  </div>
                                ) : (
                                  <MarkdownRenderer content={mainContent} />
                                )}

                                {message.suggestedQuestions && message.suggestedQuestions.length > 0 && (
                                  <div className="mt-6 space-y-3 animate-fade-in">
                                    <div className="flex items-center gap-2 text-xs font-semibold text-primary/70 uppercase tracking-wider ml-1">
                                      <Sparkles className="h-3 w-3" />
                                      <span>Explore Further</span>
                                    </div>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                                      {message.suggestedQuestions.map((q, i) => (
                                        <button
                                          key={i}
                                          onClick={() => handleQuestionClick(q)}
                                          className="text-left p-3 rounded-xl border border-border/60 bg-muted/20 hover:bg-primary/5 hover:border-primary/30 hover:shadow-sm transition-all group flex items-start gap-2.5 transition-all duration-200"
                                        >
                                          <div className="mt-1 h-1.5 w-1.5 rounded-full bg-primary/40 group-hover:bg-primary flex-shrink-0" />
                                          <span className="text-sm text-foreground/80 group-hover:text-primary font-medium leading-snug">{q}</span>
                                        </button>
                                      ))}
                                    </div>
                                  </div>
                                )}

                                {referencesContent && (
                                  <div className="border border-border/50 rounded-lg overflow-hidden bg-muted/30 mt-4">
                                    <details className="group">
                                      <summary className="flex items-center justify-between px-4 py-2.5 cursor-pointer bg-muted/50 hover:bg-muted transition-colors">
                                        <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
                                          <BookOpen className="h-3.5 w-3.5" />
                                          <span>View Reference Sources</span>
                                        </div>
                                        <div className="transform transition-transform group-open:rotate-180">
                                          <svg width="10" height="6" viewBox="0 0 10 6" fill="none" className="text-muted-foreground">
                                            <path d="M1 1L5 5L9 1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                          </svg>
                                        </div>
                                      </summary>
                                      <div className="p-4 pt-2 text-xs text-muted-foreground border-t border-border/50 bg-background/50">
                                        <MarkdownRenderer content={referencesContent} />
                                      </div>
                                    </details>
                                  </div>
                                )}
                              </div>
                            );
                          })()
                        )}
                      </div>

                      {message.role === "assistant" && (
                        <div className="absolute -bottom-6 left-0 flex gap-2">
                          <button
                            onClick={() => {
                              const cleanText = message.content.split("### 📚 Reference Chunks")[0];
                              speak(cleanText);
                            }}
                            className="text-muted-foreground hover:text-foreground p-1 transition-colors flex items-center gap-1.5 hover:bg-muted/50 rounded-md px-2"
                            title="Read Aloud"
                          >
                            <Volume2 className="h-3.5 w-3.5" />
                            <span className="text-xs">Read</span>
                          </button>
                        </div>
                      )}
                    </div>

                    {message.role === "user" && (
                      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center shadow-sm">
                        <User className="h-4 w-4 text-primary-foreground" />
                      </div>
                    )}
                  </div>
                ))}

                {isLoading && (
                  <div className="flex gap-4 justify-start">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center border border-blue-200">
                      <Bot className="h-5 w-5 text-blue-600" />
                    </div>
                    <div className="bg-card border border-border/60 rounded-2xl rounded-tl-sm px-5 py-4 shadow-sm">
                      <div className="flex items-center gap-2.5">
                        <Loader2 className="h-4 w-4 animate-spin text-primary" />
                        <span className="text-sm font-medium text-muted-foreground">Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Bottom Input Area */}
            <div className="border-t border-border bg-background/95 backdrop-blur p-4 pb-6">
              <div className="max-w-6xl mx-auto">
                <form onSubmit={handleSubmit} className="relative flex items-end gap-2 bg-muted/30 rounded-2xl border border-border p-2 focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                  <Textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={subject ? `Ask a follow-up question on ${subject}...` : "Ask a follow-up question..."}
                    className="min-h-[44px] max-h-[150px] w-full resize-none border-0 focus-visible:ring-0 bg-transparent px-3 py-2.5 pl-10 pr-20"
                    rows={1}
                  />

                  {/* Image Preview in Bottom Bar */}
                  {imagePreview && (
                    <div className="absolute -top-16 left-0 bg-background/95 backdrop-blur p-2 rounded-lg border border-border shadow-sm">
                      <div className="relative">
                        <img src={imagePreview} alt="Preview" className="h-12 w-auto rounded border border-border/50 object-cover" />
                        <button
                          onClick={clearImage}
                          className="absolute -top-2 -right-2 bg-background rounded-full p-0.5 border border-border shadow-sm hover:bg-muted"
                        >
                          <X className="h-3 w-3 text-muted-foreground" />
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Left Action (Upload) */}
                  <div className="absolute left-2 bottom-2">
                    <input
                      type="file"
                      ref={fileInputRef}
                      accept="image/*"
                      className="hidden"
                      onChange={handleImageSelect}
                    />
                    <Button
                      type="button"
                      size="icon"
                      variant="ghost"
                      onClick={() => fileInputRef.current?.click()}
                      className={`h-8 w-8 rounded-lg ${selectedImage ? 'text-primary bg-primary/10' : 'text-muted-foreground hover:text-foreground'}`}
                    >
                      <Paperclip className="h-4 w-4" />
                    </Button>
                  </div>

                  <div className="flex items-center gap-1 pb-1">
                    <Button
                      type="button"
                      size="icon"
                      variant="ghost"
                      onClick={toggleRecording}
                      className={`h-8 w-8 rounded-lg ${isRecording ? 'text-red-500 bg-red-50' : 'text-muted-foreground hover:text-foreground'}`}
                    >
                      {isRecording ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                    </Button>
                    <Button
                      type="submit"
                      size="icon"
                      disabled={!input.trim() || isLoading}
                      className="h-8 w-8 rounded-lg bg-primary hover:bg-primary/90 text-primary-foreground shadow-sm"
                    >
                      <Send className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                </form>
                <div className="text-center mt-2">
                  <p className="text-[10px] text-muted-foreground/60">
                    Responses are generated using course-aligned materials. Verify results for examinations.
                  </p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Chat;
