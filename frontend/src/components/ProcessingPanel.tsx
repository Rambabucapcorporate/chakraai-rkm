import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { 
  Play, 
  FileText, 
  Sparkles, 
  Database,
  GraduationCap,
  BookOpen,
  Calendar,
  MessageSquare
} from "lucide-react";
import { FileItem } from "./FileExplorer";

interface ProcessingPanelProps {
  selectedFile: FileItem | null;
}

interface AnalysisData {
  fileName: string;
  year: string;
  branch: string;
  semester: string;
  subject: string;
  query: string;
}

const ProcessingPanel = ({ selectedFile }: ProcessingPanelProps) => {
  const [year, setYear] = useState("");
  const [branch, setBranch] = useState("");
  const [semester, setSemester] = useState("");
  const [subject, setSubject] = useState("");
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [knowledgeBaseName, setKnowledgeBaseName] = useState("");

  // Auto-populate knowledge base name when file is selected
  useEffect(() => {
    if (selectedFile) {
      // Remove file extension for cleaner name
      const nameWithoutExt = selectedFile.name.replace(/\.[^/.]+$/, "");
      setKnowledgeBaseName(nameWithoutExt);
    } else {
      setKnowledgeBaseName("");
    }
  }, [selectedFile]);

  const handleRunAnalysis = async () => {
    if (!selectedFile) return;

    setIsLoading(true);

    // Structure all form data into JSON object
    const analysisData: AnalysisData = {
      fileName: selectedFile.name,
      year,
      branch,
      semester,
      subject,
      query,
    };

    // Log the JSON object (ready for FastAPI backend integration)
    console.log("=== Analysis Request JSON ===");
    console.log(JSON.stringify(analysisData, null, 2));
    console.log("============================");

    // Mock API call delay
    await new Promise((resolve) => setTimeout(resolve, 2000));

    setIsLoading(false);

    // Show success in console
    console.log("Analysis request ready for FastAPI backend");
  };

  const isFormValid = selectedFile && year && branch && semester && subject && query;

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="gradient-primary p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-primary-foreground/10 backdrop-blur-sm">
            <Sparkles className="h-6 w-6 text-primary-foreground" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-primary-foreground">Processing Panel</h2>
            <p className="text-sm text-primary-foreground/80">Configure and run your analysis</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
        <div className="max-w-2xl mx-auto space-y-6">
          {/* Selected File Display */}
          <div className="glass-card rounded-xl p-5 shadow-elegant">
            <div className="flex items-center gap-3 mb-4">
              <Database className="h-5 w-5 text-primary" />
              <h3 className="font-semibold">Knowledge Base</h3>
            </div>
            
            <div className="space-y-3">
              <div>
                <Label className="text-sm text-muted-foreground">Selected Source</Label>
                <div className="mt-1.5 flex items-center gap-2 p-3 bg-muted/50 rounded-lg border border-border">
                  <FileText className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm font-medium">
                    {selectedFile ? selectedFile.name : "No file selected"}
                  </span>
                </div>
              </div>
              
              <div>
                <Label htmlFor="kbName" className="text-sm text-muted-foreground">
                  Knowledge Base Name
                </Label>
                <Input
                  id="kbName"
                  value={knowledgeBaseName}
                  onChange={(e) => setKnowledgeBaseName(e.target.value)}
                  placeholder="Auto-populated from file name"
                  className="mt-1.5 input-focus"
                  disabled={!selectedFile}
                />
              </div>
            </div>
          </div>

          {/* Metadata Form */}
          <div className="glass-card rounded-xl p-5 shadow-elegant">
            <div className="flex items-center gap-3 mb-4">
              <GraduationCap className="h-5 w-5 text-primary" />
              <h3 className="font-semibold">Academic Metadata</h3>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-sm flex items-center gap-2">
                  <Calendar className="h-3.5 w-3.5" />
                  Year
                </Label>
                <Select value={year} onValueChange={setYear}>
                  <SelectTrigger className="input-focus">
                    <SelectValue placeholder="Select year" />
                  </SelectTrigger>
                  <SelectContent className="bg-popover border border-border shadow-lg z-50">
                    <SelectItem value="1st">1st Year</SelectItem>
                    <SelectItem value="2nd">2nd Year</SelectItem>
                    <SelectItem value="3rd">3rd Year</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-sm flex items-center gap-2">
                  <BookOpen className="h-3.5 w-3.5" />
                  Semester
                </Label>
                <Select value={semester} onValueChange={setSemester}>
                  <SelectTrigger className="input-focus">
                    <SelectValue placeholder="Select semester" />
                  </SelectTrigger>
                  <SelectContent className="bg-popover border border-border shadow-lg z-50">
                    <SelectItem value="1">Semester 1</SelectItem>
                    <SelectItem value="2">Semester 2</SelectItem>
                    <SelectItem value="3">Semester 3</SelectItem>
                    <SelectItem value="4">Semester 4</SelectItem>
                    <SelectItem value="5">Semester 5</SelectItem>
                    <SelectItem value="6">Semester 6</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="branch" className="text-sm">Branch / Department</Label>
                <Input
                  id="branch"
                  value={branch}
                  onChange={(e) => setBranch(e.target.value)}
                  placeholder="e.g., Computer Science"
                  className="input-focus"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="subject" className="text-sm">Subject</Label>
                <Input
                  id="subject"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g., Data Structures"
                  className="input-focus"
                />
              </div>
            </div>
          </div>

          {/* Query Section */}
          <div className="glass-card rounded-xl p-5 shadow-elegant">
            <div className="flex items-center gap-3 mb-4">
              <MessageSquare className="h-5 w-5 text-primary" />
              <h3 className="font-semibold">Analysis Query</h3>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="query" className="text-sm text-muted-foreground">
                What would you like to know?
              </Label>
              <Textarea
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your question or analysis request..."
                className="min-h-[120px] input-focus resize-none"
              />
            </div>
          </div>

          {/* Run Button */}
          <Button
            variant="gradient"
            size="xl"
            className="w-full"
            onClick={handleRunAnalysis}
            disabled={!isFormValid || isLoading}
          >
            {isLoading ? (
              <div className="flex items-center gap-3">
                <div className="h-5 w-5 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                <span>Running Analysis...</span>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Play className="h-5 w-5" />
                <span>Run Analysis</span>
              </div>
            )}
          </Button>

          {/* Info text */}
          <p className="text-center text-sm text-muted-foreground">
            {!selectedFile && "Please select a file from the Knowledge Base to begin."}
            {selectedFile && !isFormValid && "Complete all fields to enable analysis."}
            {isFormValid && "Ready to run analysis. Check browser console for JSON output."}
          </p>
        </div>
      </div>

      {/* Footer Quote */}
      <div className="border-t border-border p-4 bg-muted/30">
        <blockquote className="quote-text text-center max-w-md mx-auto">
          "All the powers in the universe are already ours. It is we who have put our hands before our eyes and cry that it is dark."
        </blockquote>
        <p className="text-xs text-muted-foreground text-center mt-1">— Swami Vivekananda</p>
      </div>
    </div>
  );
};

export default ProcessingPanel;
