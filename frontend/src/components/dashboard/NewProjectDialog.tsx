import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useProjectStore } from '@/stores/projectStore';
import { useNavigate } from 'react-router-dom';
import { stylePresets } from '@/lib/mockData';
import { cn } from '@/lib/utils';
import { Plus, Sparkles } from 'lucide-react';

interface NewProjectDialogProps {
  children?: React.ReactNode;
}

export function NewProjectDialog({ children }: NewProjectDialogProps) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [template, setTemplate] = useState('lovable');
  const { createProject, setCurrentProject } = useProjectStore();
  const navigate = useNavigate();

  const handleCreate = () => {
    if (!name.trim()) return;
    
    const project = createProject(name, description, template);
    setCurrentProject(project);
    setOpen(false);
    setName('');
    setDescription('');
    navigate(`/editor/${project.id}`);
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children || (
          <Button className="gap-2">
            <Plus className="w-4 h-4" />
            New Project
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-primary" />
            Create New Project
          </DialogTitle>
          <DialogDescription>
            Start a new Flutter project with AI-powered code generation.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Project Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="My Awesome App"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="A brief description of your app..."
              rows={2}
            />
          </div>

          <div className="space-y-2">
            <Label>Style Template</Label>
            <div className="grid grid-cols-2 gap-3">
              {stylePresets.map((preset) => (
                <button
                  key={preset.id}
                  onClick={() => setTemplate(preset.id)}
                  className={cn(
                    'p-4 rounded-lg border-2 text-left transition-all',
                    template === preset.id
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:border-primary/50'
                  )}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xl">{preset.icon}</span>
                    <span className="font-medium">{preset.name}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {preset.description}
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button onClick={handleCreate} disabled={!name.trim()}>
            Create Project
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
