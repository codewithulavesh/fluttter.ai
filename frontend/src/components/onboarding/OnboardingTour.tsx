import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Sparkles, Zap, Eye, Download, ChevronRight } from 'lucide-react';

const tourSteps = [
  {
    title: 'Welcome to FlutterAI Playground',
    description: 'Create stunning Flutter UIs from natural language descriptions. Let AI transform your ideas into beautiful, production-ready code.',
    icon: Sparkles,
    color: 'text-primary',
  },
  {
    title: 'Create Your Project',
    description: 'Start by creating a new project. Choose from style templates like Lovable, Material, or Minimal to match your design preferences.',
    icon: Zap,
    color: 'text-yellow-500',
  },
  {
    title: 'Describe Your UI',
    description: 'Enter a natural language prompt describing the Flutter UI you want. Our AI will generate multiple variants for you to choose from.',
    icon: Eye,
    color: 'text-blue-500',
  },
  {
    title: 'Preview & Export',
    description: 'See your generated code in a live device simulator. When you\'re happy, export your complete Flutter project as a ZIP file.',
    icon: Download,
    color: 'text-green-500',
  },
];

interface OnboardingTourProps {
  onComplete: () => void;
}

export function OnboardingTour({ onComplete }: OnboardingTourProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isOpen, setIsOpen] = useState(true);

  const handleNext = () => {
    if (currentStep < tourSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setIsOpen(false);
      localStorage.setItem('flutterai-onboarding-complete', 'true');
      onComplete();
    }
  };

  const handleSkip = () => {
    setIsOpen(false);
    localStorage.setItem('flutterai-onboarding-complete', 'true');
    onComplete();
  };

  const step = tourSteps[currentStep];
  const Icon = step.icon;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="sm:max-w-[450px] p-0 overflow-hidden">
        {/* Header Visual */}
        <div className="h-48 bg-gradient-to-br from-primary/20 via-primary/10 to-accent/20 flex items-center justify-center relative">
          <div className="absolute inset-0 opacity-30">
            {[...Array(20)].map((_, i) => (
              <div
                key={i}
                className="absolute w-2 h-2 rounded-full bg-primary"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  opacity: Math.random() * 0.5 + 0.2,
                  animation: `pulse ${2 + Math.random() * 2}s infinite`,
                }}
              />
            ))}
          </div>
          <div className={cn('w-20 h-20 rounded-2xl bg-card shadow-lg flex items-center justify-center', step.color)}>
            <Icon className="w-10 h-10" />
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          <div className="text-center space-y-2">
            <h2 className="text-xl font-semibold">{step.title}</h2>
            <p className="text-muted-foreground">{step.description}</p>
          </div>

          {/* Progress Dots */}
          <div className="flex justify-center gap-2">
            {tourSteps.map((_, i) => (
              <div
                key={i}
                className={cn(
                  'w-2 h-2 rounded-full transition-all',
                  i === currentStep ? 'w-6 bg-primary' : 'bg-muted'
                )}
              />
            ))}
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <Button variant="outline" onClick={handleSkip} className="flex-1">
              Skip Tour
            </Button>
            <Button onClick={handleNext} className="flex-1 gap-2">
              {currentStep === tourSteps.length - 1 ? (
                'Get Started'
              ) : (
                <>
                  Next
                  <ChevronRight className="w-4 h-4" />
                </>
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
