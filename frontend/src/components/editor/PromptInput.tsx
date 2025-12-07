import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { useProjectStore } from '@/stores/projectStore';
import { stylePresets } from '@/lib/mockData';
import { cn } from '@/lib/utils';
import { 
  Sparkles, 
  Mic, 
  Settings2, 
  Zap,
  Loader2
} from 'lucide-react';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';

export function PromptInput() {
  const [prompt, setPrompt] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('lovable');
  const [temperature, setTemperature] = useState([0.7]);
  const [variantCount, setVariantCount] = useState([3]);
  const { generateVariants, isGenerating } = useProjectStore();

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    await generateVariants(prompt);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.metaKey) {
      handleGenerate();
    }
  };

  return (
    <div className="border-b border-border bg-card p-4 space-y-4">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="w-5 h-5 text-primary" />
        <h3 className="font-medium">AI Prompt</h3>
      </div>

      {/* Style Presets */}
      <div className="flex flex-wrap gap-2">
        {stylePresets.map((preset) => (
          <button
            key={preset.id}
            onClick={() => setSelectedStyle(preset.id)}
            className={cn(
              'px-3 py-1.5 rounded-full text-sm flex items-center gap-1.5 transition-all',
              selectedStyle === preset.id
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted hover:bg-muted/80 text-foreground'
            )}
          >
            <span>{preset.icon}</span>
            <span>{preset.name}</span>
          </button>
        ))}
      </div>

      {/* Prompt Textarea */}
      <div className="relative">
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe the Flutter UI you want to create... (⌘+Enter to generate)"
          className="min-h-[100px] pr-24 resize-none"
        />
        <div className="absolute right-2 bottom-2 flex items-center gap-1">
          <Button variant="ghost" size="icon" className="h-8 w-8">
            <Mic className="w-4 h-4" />
          </Button>
          
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <Settings2 className="w-4 h-4" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-72" align="end">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label className="text-sm">Temperature: {temperature[0]}</Label>
                  <Slider
                    value={temperature}
                    onValueChange={setTemperature}
                    min={0}
                    max={1}
                    step={0.1}
                  />
                  <p className="text-xs text-muted-foreground">
                    Higher = more creative, Lower = more precise
                  </p>
                </div>
                <div className="space-y-2">
                  <Label className="text-sm">Variants: {variantCount[0]}</Label>
                  <Slider
                    value={variantCount}
                    onValueChange={setVariantCount}
                    min={1}
                    max={5}
                    step={1}
                  />
                </div>
              </div>
            </PopoverContent>
          </Popover>
        </div>
      </div>

      {/* Generate Button */}
      <Button 
        onClick={handleGenerate} 
        disabled={!prompt.trim() || isGenerating}
        className="w-full gap-2"
      >
        {isGenerating ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Generating...
          </>
        ) : (
          <>
            <Zap className="w-4 h-4" />
            Generate UI
          </>
        )}
      </Button>
    </div>
  );
}
