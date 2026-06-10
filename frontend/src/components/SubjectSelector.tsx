import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  GraduationCap,
  BookOpen,
  Calendar,
  Layers,
  ArrowRight,
  Sparkles,
  Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";
import { API_BASE_URL } from "@/lib/api";

// ACADEMIC_CONFIG matching backend structure
const ACADEMIC_CONFIG: Record<string, Record<string, Record<string, string[]>>> = {
  "Bachelor of Commerce (Accounting & Finance)": {
    "1st Year": {
      "Semester 1": [
        "Principles of Financial Accounting",
        "Business Management",
        "Business Statistics & Operations"
      ],
      "Semester 2": [
        "Advanced Financial Accounting",
        "Banking & Financial System",
        "Business Arithmetic & Logical"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "Corporate Accounting",
        "International Accounting Standards and Reporting",
        "Foreign Exchange & Financing for Foreign Trade",
        "Accounting for Decision Making",
        "Business & Corporate Law"
      ],
      "Semester 4": [
        "Advanced Corporate Accounting",
        "Indirect Taxation",
        "Principles of Financial Management",
        "Fiscal Economics",
        "Auditing – Theory & Applications"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "Advanced Financial Management",
        "Principles of Cost Accounting",
        "Direct Taxes - I",
        "Computerized Accounting",
        "Research Methodology"
      ],
      "Semester 6": [
        "Advanced Cost Accounting",
        "Investment Management",
        "Direct Taxes - II",
        "Management of Lending",
        "International Financial Management"
      ]
    }
  },
  "Bachelor of Commerce (General)": {
    "1st Year": {
      "Semester 1": [
        "Financial Accounting - I",
        "Quantitative Techniques",
        "Business Economics"
      ],
      "Semester 2": [
        "Development Economics",
        "Quantitative Techniques",
        "Financial Accounting - II"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "CORPORATE ACCOUNTING I ",
        "Banking Theory",
        "Corporate Governance"
      ],
      "Semester 4": [
        "CORPORATE ACCOUNTING II"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "Auditing",
        "Cost Accounting",
        "Income Tax"
      ],
      "Semester 6": [
        "Income Tax"
      ]
    }
  },
  "Bachelor of Business Administration": {
    "1st Year": {
      "Semester 1": [
        "Marketing Management"
      ],
      "Semester 2": [
        "Management Process"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "Production and Materials Management",
        "Accounting For Management - I"
      ],
      "Semester 4": [
        "Logistics and Supply Chain Management",
        "Accounting For Management - II"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "Entrepreneurship and Project Management",
        "Strategic Management",
        "Capital Markets & Investment Management",
        "Business Research Methods",
        "Business Communications and Managerial Skills",
        "Business Finance",
        "Business Taxation"
      ]
    }
  },
  "Bachelor of Commerce (Computer Applications)": {
    "1st Year": {
      "Semester 1": [
        "Computer Application in E-commerce"
      ],
      "Semester 2": [
        "Corporate Accounting And Audting",
        "Office Automation Package"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "Modern Management Techniques",
        "Quantitative Applications for Business-1",
        "Relational Database Management System"
      ],
      "Semester 4": [
        "Data Analytics with R Programming",
        "Business Finance",
        "Legal Application in Business",
        "Quantitative Applications for Business- II",
        "Software Development with Visual Basic"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "Internet in Web Technology",
        "Problem Solving using Python",
        "Marketing Research for Business",
        "Recent Trends in Human Resource Management",
        "Taxation and its Application"
      ],
      "Semester 6": [
        "Computerized Accounting Application",
        "Blockchain Technology in Cryptocurrency",
        "Entrepreneurial Development",
        "Goods & Service Tax ",
        "Banking and financial Service"
      ]
    }
  },
  "Bachelor of Computer Applications": {
    "1st Year": {
      "Semester 1": [
        "C Programming (T+P)",
        "Operating Systems (T+P)"
      ],
      "Semester 2": [
        "Data Structures and Algorithms (T+P)",
        "Object Oriented Programming (T+P)",
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "Java Programming(T+P)",
        "Relational Database Management System (T+ P)",
        "Digital Image Processing",
        "Computer Networks and Cyber Security"
      ],
      "Semester 4": [
        "Distributed Databaase Management Systems",
        "Advanced Java",
        "Java Full Stack",
        "Cloud Computing",
        "Web Technology"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "PHP Programming (T+P)",
        "Mobile Applications Development (T+P)",
        "Data Mining and Data Warehousing (E1)",
        "Software Engineering (E2)"
      ],
      "Semester 6": [
        "Big Data Analytics",
        "R Programming (T+P)",
        "Deep Learning",
        "IoT",
        "GEN AI"
      ]
    }
  },
  "Bachelor of Computer Science": {
    "1st Year": {
      "Semester 1": [
        "C Programming (T+P)",
        "Operating Systems (T+P)"
      ],
      "Semester 2": [
        "Data Structures and Algorithms (T+P)"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "Java Programming (T+P)",
        "Relational Database Management System (T+P)",
      ],
      "Semester 4": [
        "Advanced Java",
        "Web Technology",
        "Distributed Databaase Management Systems",
        "Java Full Stack",
        "Cloud Computing"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "PHP Programming (T+P)",
        "Mobile Applications Development (T+P)",
        "Data Mining and Data Warehousing (E1)",
        "Software Engineering (E2)"
      ],
      "Semester 6": [
        "Internet of Things (IoT)",
        "Big Data Analytics",
        "Cloud Computing",
        "R Programming (T+P)",
        "Deep Learning"
      ]
    }
  },
  "Bachelor of Commerce (Banking Management)": {
    "1st Year": {
      "Semester 1": [
        "Principles of Financial Accounting",
        "Business Management",
        "Business Statistics & Operations"
      ],
      "Semester 2": [
        "Advanced Financial Accounting",
        "Banking Management Theory",
        "Business Arithmetic & Logical"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "Company Accounts",
        "Accounting for Decision Making",
        "Human Resource Management",
        "Business & Corporate Law",
        "Auditing – Theory & Applications"
      ],
      "Semester 4": [
        "Principles of Financial Management",
        "Insurance Theory and Accounting",
        "Banking Law",
        "International Banking",
        "Monetary Economics"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "Taxation - I",
        "Theory of Research Analysis",
        "Banking Advances",
        "Capital Markets and Financial Service",
        "Computerized Accounting"
      ],
      "Semester 6": [
        "Principles and Practices of Costing",
        "Taxation - II",
        "E - Banking and Cyber Laws",
        "Treasury Management",
        "Investment Management",
        "Finanacial Management"
      ]
    }
  },
  "Bachelor of Commerce (CS)": {
    "1st Year": {
      "Semester 1": [
        "ADVANCED ACCOUNTANCY I & II",
        "BUSINESS REGULATORY FRAMEWORK",
        "Mercantile & Contract Law"
      ],
      "Semester 2": [
        "ECONOMIC & COMMERCIAL LAWS",
        "ADVANCED ACCOUNTANCY I & II"
      ]
    },
    "2nd Year": {
      "Semester 3": [
        "ACCOUNTING FOR COMPANIES I & II",
        "COMPANY LAW AND SECRETARIAL PRACTICE I & II",
        "ETHICAL MANAGEMENT THEORY",
        "DIGITAL DATA PROTECTION"
      ],
      "Semester 4": [
        "AUDITING AND ASSURANCE",
        "SECURITIES LAWS AND FINANCIAL MARKETS",
        "DRAFTING AND PLEADING ETQUETTE"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "ELEMENTS OF BUSINESS TAXATION",
        "ENTREPRENEURSHIP & SMALL BUSINESS MANAGEMENT",
        "INDUSTRIAL & LABOUR LAWS",
        "PRINCIPLES OF COSTING"
      ],
      "Semester 6": [
        "PRINCIPLES OF MANAGEMENT ACCOUNTING",
        "CORPORATE FINANCE",
        "CORPORATE HRM",
        "PRINCIPLES OF INCOME TAX I & II"
      ]
    },
  },
  "Bachelor of Commerce (ISM)": {
    "1st Year": {
      "Semester 1": [
        "Financial Accounting"
      ],
      "Semester 2": [
        "Corporate Accounting"
      ]
    },
    "3rd Year": {
      "Semester 5": [
        "Direct Taxation"
      ]
    }
  }
};

const branches = [
  "Bachelor of Commerce (Accounting & Finance)",
  "Bachelor of Commerce (General)",
  "Bachelor of Business Administration",
  "Bachelor of Commerce (Computer Applications)",
  "Bachelor of Computer Applications",
  "Bachelor of Computer Science",
  "Bachelor of Commerce (Banking Management)",
  "Bachelor of Commerce (CS)",
  "Bachelor of Commerce (ISM)"
];

const SubjectSelector = () => {
  const navigate = useNavigate();
  const [year, setYear] = useState("");
  const [branch, setBranch] = useState("");
  const [semester, setSemester] = useState("");
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Get available semesters based on year
  const getAvailableSemesters = () => {
    if (year === "1st Year") return ["Semester 1", "Semester 2"];
    if (year === "2nd Year") return ["Semester 3", "Semester 4"];
    if (year === "3rd Year") return ["Semester 5", "Semester 6"];
    return [];
  };

  // Get subjects based on selections
  const getSubjects = (): string[] => {
    if (!year || !branch || !semester) return [];
    return ACADEMIC_CONFIG[branch]?.[year]?.[semester] || [];
  };

  const subjects = getSubjects();

  const handleSubjectClick = (subject: string) => {
    setSelectedSubject(subject);
  };

  const handleStartChat = async () => {
    if (!selectedSubject) return;

    setIsLoading(true);

    try {
      // triggered load data
      // const response = await fetch("https://apichakra.rkmvc.ac.in/api/set_subject", {
      const response = await fetch(`${API_BASE_URL}/api/set_subject`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          year,
          branch,
          semester,
          subject: selectedSubject,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to load subject data");
      }

      // Only navigate after successful loading
      const params = new URLSearchParams({
        year,
        branch,
        semester,
        subject: selectedSubject,
      });

      navigate(`/chat?${params.toString()}`);
    } catch (error) {
      console.error("Error loading subject data:", error);
      alert("Failed to load subject data. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Reset downstream selections when upstream changes
  const handleYearChange = (value: string) => {
    setYear(value);
    setSemester("");
    setSelectedSubject(null);
  };

  const handleBranchChange = (value: string) => {
    setBranch(value);
    setSelectedSubject(null);
  };

  const handleSemesterChange = (value: string) => {
    setSemester(value);
    setSelectedSubject(null);
  };

  return (
    <div className="h-full overflow-y-auto bg-background scrollbar-thin">
      <div className="min-h-full flex flex-col">
        {/* Content */}
        <div className="flex-1 p-6">
          <div className="max-w-2xl mx-auto space-y-6">
            {/* Filters Card */}
            <div className="glass-card rounded-xl p-5 shadow-elegant">
              <div className="flex items-center gap-3 mb-5">
                <Layers className="h-5 w-5 text-primary" />
                <h3 className="font-semibold">Course Details</h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label className="text-sm flex items-center gap-2">
                    <Calendar className="h-3.5 w-3.5" />
                    Year
                  </Label>
                  <Select value={year} onValueChange={handleYearChange}>
                    <SelectTrigger className="input-focus">
                      <SelectValue placeholder="Select year" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover border border-border shadow-lg z-50">
                      <SelectItem value="1st Year">1st Year</SelectItem>
                      <SelectItem value="2nd Year">2nd Year</SelectItem>
                      <SelectItem value="3rd Year">3rd Year</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm flex items-center gap-2">
                    <GraduationCap className="h-3.5 w-3.5" />
                    Branch
                  </Label>
                  <Select value={branch} onValueChange={handleBranchChange}>
                    <SelectTrigger className="input-focus">
                      <SelectValue placeholder="Select branch" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover border border-border shadow-lg z-50">
                      {branches.map((b) => (
                        <SelectItem key={b} value={b}>{b}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label className="text-sm flex items-center gap-2">
                    <BookOpen className="h-3.5 w-3.5" />
                    Semester
                  </Label>
                  <Select
                    value={semester}
                    onValueChange={handleSemesterChange}
                    disabled={!year}
                  >
                    <SelectTrigger className="input-focus">
                      <SelectValue placeholder="Select semester" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover border border-border shadow-lg z-50">
                      {getAvailableSemesters().map((s) => (
                        <SelectItem key={s} value={s}>{s}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>

            {/* Subjects Grid */}
            {subjects.length > 0 && (
              <div className="glass-card rounded-xl p-5 shadow-elegant animate-fade-in">
                <div className="flex items-center gap-3 mb-5">
                  <Sparkles className="h-5 w-5 text-primary" />
                  <h3 className="font-semibold">Available Subjects</h3>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {subjects.map((subject) => (
                    <button
                      key={subject}
                      onClick={() => handleSubjectClick(subject)}
                      className={cn(
                        "p-4 rounded-xl border-2 text-left transition-all duration-200",
                        "hover:shadow-md hover:scale-[1.02]",
                        selectedSubject === subject
                          ? "border-primary bg-primary/5 shadow-md"
                          : "border-border bg-card hover:border-primary/50"
                      )}
                    >
                      <div className="flex items-start gap-3">
                        <div className={cn(
                          "p-2 rounded-lg",
                          selectedSubject === subject ? "bg-primary/10" : "bg-muted"
                        )}>
                          <BookOpen className={cn(
                            "h-5 w-5",
                            selectedSubject === subject ? "text-primary" : "text-muted-foreground"
                          )} />
                        </div>
                        <div>
                          <p className={cn(
                            "font-medium",
                            selectedSubject === subject ? "text-primary" : "text-foreground"
                          )}>
                            {subject}
                          </p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {branch} • {semester}
                          </p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Empty state */}
            {year && branch && semester && subjects.length === 0 && (
              <div className="text-center py-12">
                <p className="text-muted-foreground">No subjects available for this combination</p>
              </div>
            )}

            {/* Start Chat Button */}
            {selectedSubject && (
              <Button
                variant="gradient"
                size="xl"
                className="w-full animate-fade-in"
                onClick={handleStartChat}
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                    <span>Loading Knowledge Base...</span>
                  </>
                ) : (
                  <>
                    <span>Start Learning {selectedSubject}</span>
                    <ArrowRight className="h-5 w-5 ml-2" />
                  </>
                )}
              </Button>
            )}
          </div>
        </div>

        {/* Footer Quote */}
        <div className="border-t border-border p-4 bg-muted/30 mt-auto">
          <blockquote className="quote-text text-center max-w-md mx-auto">
            "All the powers in the universe are already ours. It is we who have put our hands before our eyes and cry that it is dark."
          </blockquote>
          <p className="text-xs text-muted-foreground text-center mt-1">— Swami Vivekananda</p>
        </div>
      </div>
    </div>
  );
};

export default SubjectSelector;
