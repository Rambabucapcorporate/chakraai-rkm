import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useNavigate } from "react-router-dom";
import { LogOut, BookOpen } from "lucide-react";
import SubjectSelector from "@/components/SubjectSelector";
import { useAuth } from "@/contexts/AuthContext";
import { API_BASE_URL } from "@/lib/api";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"idle" | "success" | "error">("idle");

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const handleFileUpload = async () => {
    if (uploadFiles.length === 0) return;

    setIsUploading(true);
    setUploadStatus("idle");

    // In a real app, we would upload the files to the backend here
    // For this demo, we simulate a delay and trigger a "reload" of knowledge base

    try {
      // Extract filenames from the uploaded File objects
      const filenames = uploadFiles.map(file => file.name);

      // const response = await fetch("https://apichakra.rkmvc.ac.in/api/load", {
      const response = await fetch(`${API_BASE_URL}/api/load`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ filenames: filenames }),
      });

      if (response.ok) {
        setUploadStatus("success");
        setTimeout(() => {
          setIsUploadOpen(false);
          setUploadStatus("idle");
          setUploadFiles([]);
        }, 2000);
      } else {
        setUploadStatus("error");
      }
    } catch (e) {
      console.error(e);
      setUploadStatus("error");
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setUploadFiles(Array.from(e.target.files));
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Header */}
      <header className="gradient-primary py-3 px-6 flex-shrink-0 z-10 shadow-md">
        <div className="relative flex items-center justify-between max-w-7xl mx-auto w-full">
          {/* Left: Branding */}
          <div className="flex items-center gap-3">
            <div className="flex-shrink-0">
              <img src="/rkm-logo.png" alt="RKM Logo" className="h-12 w-auto object-contain bg-white/10 rounded-lg p-1" />
            </div>
            <div className="flex flex-col">
              <h1 className="text-lg font-bold text-white leading-tight tracking-wide">
                Knowledge Retrieval System
              </h1>
              <p className="text-xs text-primary-foreground/80 font-medium hidden sm:block">
                Ramakrishna Mission Vivekananda College
              </p>
            </div>
          </div>

          {/* Center: Hero Title */}
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-center hidden md:block">
            <h2 className="text-xl font-bold text-white tracking-tight leading-none drop-shadow-md">Select Your Subject</h2>
            <p className="text-[11px] text-white/90 font-medium mt-0.5 drop-shadow-sm tracking-wide">Choose your course details below</p>
          </div>

          {/* Right: Actions & User Profile */}
          <div className="flex items-center gap-4">


            {/* User Profile Pill */}
            <div className="flex items-center gap-0 bg-white/10 backdrop-blur-md rounded-full border border-white/20 p-1 pl-4 transition-all hover:bg-white/15">
              <div className="flex flex-col text-right mr-3 hidden sm:flex">
                <span className="text-[10px] uppercase tracking-wider text-primary-foreground/70 font-bold">Logged in as</span>
                <span className="text-sm font-bold text-white leading-none">{user?.username || "Student"}</span>
              </div>
              <div className="h-8 w-[1px] bg-white/20 mx-1 hidden sm:block"></div>
              <Button
                variant="ghost"
                size="icon"
                onClick={handleLogout}
                className="rounded-full text-white hover:bg-white/20 hover:text-white w-9 h-9"
                title="Logout"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <SubjectSelector />
      </main>
    </div>
  );
};

export default Dashboard;
