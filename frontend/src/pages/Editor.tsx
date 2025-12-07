import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AppHeader } from '@/components/layout/AppHeader';
import { FileExplorer } from '@/components/editor/FileExplorer';
import { PromptInput } from '@/components/editor/PromptInput';
import { CodeEditor } from '@/components/editor/CodeEditor';
import { VariantGallery } from '@/components/editor/VariantGallery';
import { DevicePreview } from '@/components/editor/DevicePreview';
import { useProjectStore } from '@/stores/projectStore';
import { toast } from 'sonner';
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable';

export default function Editor() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const { projects, currentProject, setCurrentProject } = useProjectStore();

  useEffect(() => {
    if (projectId) {
      const project = projects.find((p) => p.id === projectId);
      if (project) {
        setCurrentProject(project);
      } else {
        toast.error('Project not found');
        navigate('/dashboard');
      }
    }
  }, [projectId, projects, setCurrentProject, navigate]);

  const handleExport = () => {
    toast.success('Project exported!', {
      description: 'Your Flutter project ZIP is downloading...',
    });
  };

  const handleRun = () => {
    toast.success('Building preview...', {
      description: 'Hot reload triggered',
    });
  };

  if (!currentProject) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Loading project...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-background">
      <AppHeader 
        showProjectActions 
        onExport={handleExport}
        onRun={handleRun}
      />

      <div className="flex-1 overflow-hidden">
        <ResizablePanelGroup direction="horizontal">
          {/* Left Panel - File Explorer */}
          <ResizablePanel defaultSize={15} minSize={10} maxSize={25}>
            <FileExplorer />
          </ResizablePanel>

          <ResizableHandle withHandle />

          {/* Middle Panel - Prompt + Code Editor + Variants */}
          <ResizablePanel defaultSize={45} minSize={30}>
            <div className="h-full flex flex-col">
              <PromptInput />
              <div className="flex-1 overflow-hidden">
                <CodeEditor />
              </div>
              <VariantGallery />
            </div>
          </ResizablePanel>

          <ResizableHandle withHandle />

          {/* Right Panel - Device Preview */}
          <ResizablePanel defaultSize={40} minSize={25}>
            <DevicePreview />
          </ResizablePanel>
        </ResizablePanelGroup>
      </div>
    </div>
  );
}
