import { Project } from '@/types';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  MoreVertical, 
  Folder,
  Calendar,
  Trash2,
  Copy,
  ExternalLink
} from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useNavigate } from 'react-router-dom';
import { useProjectStore } from '@/stores/projectStore';

interface ProjectCardProps {
  project: Project;
}

export function ProjectCard({ project }: ProjectCardProps) {
  const navigate = useNavigate();
  const { deleteProject, setCurrentProject } = useProjectStore();

  const handleOpen = () => {
    setCurrentProject(project);
    navigate(`/editor/${project.id}`);
  };

  const getTemplateEmoji = (template: string) => {
    const emojis: Record<string, string> = {
      material: '🎨',
      minimal: '✨',
      lovable: '💜',
      playful: '🎮',
    };
    return emojis[template] || '📁';
  };

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 hover:border-primary/50 overflow-hidden">
      {/* Preview Area */}
      <div 
        className="h-36 bg-gradient-to-br from-primary/10 via-primary/5 to-accent/10 flex items-center justify-center cursor-pointer relative"
        onClick={handleOpen}
      >
        <div className="w-16 h-16 rounded-2xl bg-card shadow-md flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
          {getTemplateEmoji(project.template)}
        </div>
        
        {/* Hover Overlay */}
        <div className="absolute inset-0 bg-primary/0 group-hover:bg-primary/5 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100">
          <Button variant="secondary" size="sm" className="gap-2">
            <ExternalLink className="w-4 h-4" />
            Open
          </Button>
        </div>
      </div>

      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <h3 className="font-semibold truncate">{project.name}</h3>
            <p className="text-sm text-muted-foreground truncate">
              {project.description}
            </p>
          </div>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8 -mt-1 -mr-2">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={handleOpen}>
                <ExternalLink className="w-4 h-4 mr-2" />
                Open
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Copy className="w-4 h-4 mr-2" />
                Duplicate
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem 
                className="text-destructive"
                onClick={() => deleteProject(project.id)}
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardContent>

      <CardFooter className="px-4 pb-4 pt-0">
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Folder className="w-3 h-3" />
            <span className="capitalize">{project.template}</span>
          </div>
          <div className="flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            <span>{new Intl.DateTimeFormat('en-GB').format(project.updatedAt)}</span>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
}
