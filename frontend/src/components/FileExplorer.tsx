import { useState } from "react";
import { 
  Folder, 
  FolderOpen, 
  FileText, 
  ChevronRight, 
  ChevronDown,
  Database,
  Search
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface FileItem {
  id: string;
  name: string;
  type: "folder" | "file";
  children?: FileItem[];
}

interface FileExplorerProps {
  onFileSelect: (file: FileItem) => void;
  selectedFile: FileItem | null;
}

// Mock file structure
const mockFiles: FileItem[] = [
  {
    id: "1",
    name: "Computer Science",
    type: "folder",
    children: [
      {
        id: "1-1",
        name: "Data Structures",
        type: "folder",
        children: [
          { id: "1-1-1", name: "Arrays_Notes.pdf", type: "file" },
          { id: "1-1-2", name: "LinkedList_Guide.pdf", type: "file" },
          { id: "1-1-3", name: "Trees_Algorithms.pdf", type: "file" },
        ],
      },
      {
        id: "1-2",
        name: "Operating Systems",
        type: "folder",
        children: [
          { id: "1-2-1", name: "Process_Management.pdf", type: "file" },
          { id: "1-2-2", name: "Memory_Allocation.pdf", type: "file" },
        ],
      },
      { id: "1-3", name: "Database_Concepts.pdf", type: "file" },
    ],
  },
  {
    id: "2",
    name: "Mathematics",
    type: "folder",
    children: [
      { id: "2-1", name: "Linear_Algebra.pdf", type: "file" },
      { id: "2-2", name: "Calculus_III.pdf", type: "file" },
      { id: "2-3", name: "Probability_Theory.pdf", type: "file" },
    ],
  },
  {
    id: "3",
    name: "Physics",
    type: "folder",
    children: [
      { id: "3-1", name: "Quantum_Mechanics.pdf", type: "file" },
      { id: "3-2", name: "Thermodynamics.pdf", type: "file" },
    ],
  },
  { id: "4", name: "General_Guidelines.pdf", type: "file" },
];

const FileTreeItem = ({
  item,
  level = 0,
  onSelect,
  selectedId,
}: {
  item: FileItem;
  level?: number;
  onSelect: (file: FileItem) => void;
  selectedId: string | null;
}) => {
  const [isOpen, setIsOpen] = useState(level === 0);
  const isSelected = selectedId === item.id;
  const isFolder = item.type === "folder";

  const handleClick = () => {
    if (isFolder) {
      setIsOpen(!isOpen);
    } else {
      onSelect(item);
    }
  };

  return (
    <div>
      <div
        onClick={handleClick}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        className={cn(
          "file-item group",
          isSelected && !isFolder && "file-item-selected"
        )}
      >
        {isFolder ? (
          <>
            {isOpen ? (
              <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" />
            ) : (
              <ChevronRight className="h-4 w-4 text-muted-foreground flex-shrink-0" />
            )}
            {isOpen ? (
              <FolderOpen className="h-4 w-4 text-sidebar-primary flex-shrink-0" />
            ) : (
              <Folder className="h-4 w-4 text-sidebar-primary flex-shrink-0" />
            )}
          </>
        ) : (
          <>
            <div className="w-4" />
            <FileText className="h-4 w-4 text-muted-foreground flex-shrink-0" />
          </>
        )}
        <span className="truncate text-sm">{item.name}</span>
      </div>
      
      {isFolder && isOpen && item.children && (
        <div className="animate-fade-in">
          {item.children.map((child) => (
            <FileTreeItem
              key={child.id}
              item={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const FileExplorer = ({ onFileSelect, selectedFile }: FileExplorerProps) => {
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <div className="h-full flex flex-col bg-sidebar text-sidebar-foreground">
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border">
        <div className="flex items-center gap-2 mb-4">
          <Database className="h-5 w-5 text-sidebar-primary" />
          <h2 className="font-semibold text-sm">Knowledge Base</h2>
        </div>
        
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search files..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9 bg-sidebar-accent border-sidebar-border text-sidebar-foreground placeholder:text-muted-foreground text-sm h-9"
          />
        </div>
      </div>

      {/* File Tree */}
      <div className="flex-1 overflow-y-auto py-2 scrollbar-thin">
        {mockFiles.map((item) => (
          <FileTreeItem
            key={item.id}
            item={item}
            onSelect={onFileSelect}
            selectedId={selectedFile?.id || null}
          />
        ))}
      </div>

      {/* Footer info */}
      <div className="p-4 border-t border-sidebar-border">
        <p className="text-xs text-muted-foreground">
          {selectedFile ? (
            <>Selected: <span className="text-sidebar-primary">{selectedFile.name}</span></>
          ) : (
            "Select a file to analyze"
          )}
        </p>
      </div>
    </div>
  );
};

export type { FileItem };
export default FileExplorer;
