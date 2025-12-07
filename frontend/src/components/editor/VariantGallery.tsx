import { useProjectStore } from '@/stores/projectStore';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Check, Copy, Sparkles } from 'lucide-react';
import { toast } from 'sonner';

export function VariantGallery() {
  const { variants, selectedVariant, selectVariant, acceptVariant, isGenerating } = useProjectStore();

  if (isGenerating) {
    return (
      <div className="h-48 border-t border-border bg-card flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="flex justify-center">
            <Sparkles className="w-8 h-8 text-primary animate-pulse" />
          </div>
          <p className="text-sm text-muted-foreground">Generating variants...</p>
          <div className="flex gap-2 justify-center">
            {[0, 1, 2].map((i) => (
              <div
                key={i}
                className="w-16 h-24 rounded-lg bg-muted animate-pulse"
                style={{ animationDelay: `${i * 200}ms` }}
              />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (variants.length === 0) {
    return null;
  }

  return (
    <div className="border-t border-border bg-card">
      <div className="p-3 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium">Generated Variants</span>
          <span className="text-xs text-muted-foreground">({variants.length})</span>
        </div>
      </div>

      <div className="p-4">
        <div className="flex gap-4 overflow-x-auto pb-2">
          {variants.map((variant) => (
            <div
              key={variant.id}
              onClick={() => selectVariant(variant)}
              className={cn(
                'flex-shrink-0 w-40 rounded-lg border-2 cursor-pointer transition-all overflow-hidden',
                selectedVariant?.id === variant.id
                  ? 'border-primary ring-2 ring-primary/20'
                  : 'border-border hover:border-primary/50'
              )}
            >
              {/* Preview Thumbnail */}
              <div className="h-28 bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
                <div className="w-20 h-20 bg-card rounded-lg shadow-sm flex items-center justify-center">
                  <span className="text-2xl">
                    {variant.thumbnail === 'variant-a' && '🅰️'}
                    {variant.thumbnail === 'variant-b' && '🅱️'}
                    {variant.thumbnail === 'variant-c' && '©️'}
                  </span>
                </div>
              </div>

              {/* Info */}
              <div className="p-2 bg-card">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium">Variant {variant.id}</span>
                  <span className="text-xs text-muted-foreground">
                    {Math.round(variant.confidence * 100)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {selectedVariant && (
          <div className="mt-4 flex gap-2">
            <Button
              onClick={() => acceptVariant(selectedVariant)}
              className="gap-2"
            >
              <Check className="w-4 h-4" />
              Accept Variant
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                navigator.clipboard.writeText(selectedVariant.code);
                toast.success('Code copied to clipboard');
              }}
              className="gap-2"
            >
              <Copy className="w-4 h-4" />
              Copy Code
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
