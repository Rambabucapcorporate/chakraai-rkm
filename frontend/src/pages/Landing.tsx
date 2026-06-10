import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen, MessageSquare, FileText, Sparkles, BookMarked, GraduationCap } from "lucide-react";

const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col bg-background font-sans">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border/40">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex-shrink-0">
              <img src="/rkm-logo.png" alt="RKM Logo" className="h-10 w-auto object-contain" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gradient">RKMVC Knowledge Hub</h1>
            </div>
          </div>
          <div className="flex items-center gap-4">

            <Button onClick={() => navigate("/auth")} className="bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/20">
              Get Started
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-6 overflow-hidden">
        <div className="absolute top-0 inset-x-0 h-[40rem] bg-gradient-to-b from-primary/5 via-primary/5 to-transparent -z-10" />
        <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[60rem] h-[60rem] bg-secondary/10 rounded-full blur-3xl -z-10" />

        <div className="max-w-4xl mx-auto text-center animate-slide-up">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 text-accent text-sm font-medium mb-6 border border-accent/20">
            <Sparkles className="h-4 w-4" />
            <span>AI-Powered Learning Assistant</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 text-foreground">
            Unlock the Power of <br />
            <span className="text-gradient animate-shimmer bg-[length:200%_auto]">
              Institutional Knowledge
            </span>
          </h1>

          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
            Interact with your academic resources like never before. Upload documents, ask questions, and get instant, accurate answers powered by advanced AI.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              size="lg"
              onClick={() => navigate("/auth")}
              className="w-full sm:w-auto text-lg h-12 px-8 bg-primary hover:bg-primary/90 shadow-xl shadow-primary/25"
            >
              Start Learning Now <ArrowRight className="ml-2 h-5 w-5" />
            </Button>

          </div>

          <div className="mt-12 pt-8 border-t border-border/40">
            <p className="text-sm font-medium text-muted-foreground mb-4">Trusted by students and faculty of</p>
            <div className="flex items-center justify-center gap-2 text-foreground/80 font-semibold">
              <GraduationCap className="h-6 w-6 text-primary" />
              Ramakrishna Mission Vivekananda College
            </div>
          </div>
        </div>
      </section>

      {/* Quote Section */}
      <section className="py-16 bg-muted/30 border-y border-border/40">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <blockquote className="text-2xl md:text-3xl font-serif text-primary/80 italic leading-relaxed">
            "Arise, Awake, and Stop Not Till The Goal Is Reached"
          </blockquote>
          <cite className="block mt-6 text-foreground font-semibold not-italic">
            — Swami Vivekananda
          </cite>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6 bg-background">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Everything you need to excel</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our platform provides comprehensive tools to manage your study materials and enhance your learning process.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<MessageSquare className="h-8 w-8 text-secondary" />}
              title="Intelligent Chat"
              description="Ask natural language questions about your documents and get precise, cited answers instantly."
            />
            <FeatureCard
              icon={<FileText className="h-8 w-8 text-primary" />}
              title="Document Analysis"
              description="Upload complete textbooks, papers, and notes. Our AI analyzes and indexes them for quick retrieval."
            />
            <FeatureCard
              icon={<BookMarked className="h-8 w-8 text-accent" />}
              title="Resource Library"
              description="Organize your study materials efficiently. Access the collective knowledge base of the department."
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-foreground text-background mt-auto">
        <div className="max-w-7xl mx-auto px-6 text-center space-y-3">
          <div className="flex items-center justify-center gap-2 mb-4">
            <BookOpen className="h-5 w-5 opacity-80" />
            <span className="font-bold text-lg">RKMVC Knowledge System</span>
          </div>
          <p className="text-white/60 text-sm">
            © {new Date().getFullYear()} Ramakrishna Mission Vivekananda College. All rights reserved.
          </p>
          <p className="text-white/50 text-xs">
            Developed by{" "}
            <a 
              href="https://capcorporate.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-white/80 hover:text-white hover:underline font-medium"
            >
              CAP Corporate AI Solutions LLP
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) => (
  <div className="p-6 rounded-2xl glass-card border border-border/50  hover:shadow-elegant transition-all duration-300 group">
    <div className="mb-4 p-3 rounded-xl bg-muted w-fit group-hover:bg-primary/5 transition-colors">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-2 text-foreground">{title}</h3>
    <p className="text-muted-foreground leading-relaxed">{description}</p>
  </div>
);

export default Landing;

