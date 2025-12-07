import { useProjectStore } from '@/stores/projectStore';
import { cn } from '@/lib/utils';

export function CodeEditor() {
  const { selectedFile, updateFileContent } = useProjectStore();

  if (!selectedFile || selectedFile.type === 'folder') {
    return (
      <div className="h-full flex items-center justify-center bg-card text-muted-foreground">
        <div className="text-center">
          <p className="text-sm">Select a file to edit</p>
          <p className="text-xs mt-1">or generate code using the AI prompt</p>
        </div>
      </div>
    );
  }

  const lines = (selectedFile.content || '').split('\n');

  return (
    <div className="h-full flex flex-col bg-card">
      {/* Tab Bar */}
      <div className="h-10 border-b border-border flex items-center px-2 gap-1">
        <div className="px-3 py-1.5 bg-background rounded-t text-sm flex items-center gap-2">
          <span className={cn(
            'w-2 h-2 rounded-full',
            selectedFile.name.endsWith('.dart') ? 'bg-blue-500' :
            selectedFile.name.endsWith('.yaml') ? 'bg-yellow-500' : 'bg-muted-foreground'
          )} />
          <span>{selectedFile.name}</span>
        </div>
      </div>

      {/* Editor Content */}
      <div className="flex-1 overflow-auto">
        <div className="flex min-h-full">
          {/* Line Numbers */}
          <div className="w-12 flex-shrink-0 bg-muted/30 text-muted-foreground text-right text-sm font-mono py-4 pr-3 select-none">
            {lines.map((_, i) => (
              <div key={i} className="h-6 leading-6">
                {i + 1}
              </div>
            ))}
          </div>

          {/* Code Content */}
          <textarea
            value={selectedFile.content || ''}
            onChange={(e) => updateFileContent(selectedFile.id, e.target.value)}
            className="flex-1 bg-transparent font-mono text-sm p-4 resize-none focus:outline-none leading-6"
            spellCheck={false}
          />
        </div>
      </div>
    </div>
  );
}
