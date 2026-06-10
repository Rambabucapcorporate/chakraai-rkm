import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/components/ui/use-toast";
import { BookOpen, Mail, Lock, ArrowRight, Sparkles, User, Shield, GraduationCap, Eye, EyeOff, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { api } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

type Role = "student" | "teacher" | "admin";

const Auth = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useNavigate();
  const { toast } = useToast();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      // Handle Login
      const data = await api.auth.login({ username, password });
      // After getting token, we need the user details
      localStorage.setItem("access_token", data.access_token);
      const userData = await api.auth.getMe();
      
      login(data.access_token, userData);
      
      toast({
        title: "Welcome back!",
        description: `Successfully logged in.`,
      });
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header with gradient */}
      <header className="gradient-primary py-4 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate("/")}>
            <div className="flex-shrink-0">
              <img src="/rkm-logo.png" alt="RKM Logo" className="h-12 w-auto object-contain bg-white/10 rounded-lg p-1" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-primary-foreground">RKMVC Knowledge System</h1>
              <p className="text-xs text-primary-foreground/80">Ramakrishna Mission Vivekananda College</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 flex items-center justify-center px-4 py-12 bg-gradient-to-br from-background via-muted/30 to-background">
        <div className="w-full max-w-md animate-slide-up">
          {/* Quote */}
          <div className="text-center mb-8">
            <blockquote className="quote-text text-foreground/70 max-w-sm mx-auto">
              "Arise, Awake, and Stop Not Till The Goal Is Reached"
            </blockquote>
            <p className="text-sm text-muted-foreground mt-2 font-medium">— Swami Vivekananda</p>
          </div>

          {/* Auth Card */}
          <div className="glass-card rounded-2xl overflow-hidden shadow-elegant">
            {/* Card top border gradient */}
            <div className="h-1.5 gradient-primary" />

            <div className="p-8">
              {/* Title */}
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-foreground">
                  Welcome Back
                </h2>
                <p className="text-sm text-muted-foreground mt-1">
                  Sign in to access the Knowledge Hub
                </p>
              </div>

              {/* Error Alert */}
              {error && (
                <Alert variant="destructive" className="mb-6 py-3 bg-destructive/5 border-destructive/20">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription className="font-medium">{error}</AlertDescription>
                </Alert>
              )}

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-5">
                
                <div className="space-y-2">
                  <Label htmlFor="username" className="text-sm font-medium">
                    Username or User ID
                  </Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="username"
                      type="text"
                      placeholder="Username or ID"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      className="pl-10 h-11 bg-background/50 border-input/60 focus:bg-background transition-colors"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="password" className="text-sm font-medium">
                      Password
                    </Label>
                  </div>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="pl-10 pr-10 h-11 bg-background/50 border-input/60 focus:bg-background transition-colors"
                      required
                      minLength={3}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>


                <Button
                  type="submit"
                  className="w-full h-11 font-medium text-base shadow-lg shadow-primary/20 hover:shadow-primary/30 transition-all duration-300 mt-2"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <span className="flex items-center gap-2">
                      <span className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Processing...
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      Sign In
                      <ArrowRight className="h-4 w-4" />
                    </span>
                  )}
                </Button>
              </form>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-4 px-6 border-t border-border bg-card/50">
        <div className="max-w-7xl mx-auto text-center space-y-2">
          <p className="text-sm text-muted-foreground">
            © 2026 Ramakrishna Mission Vivekananda College
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Auth;
