import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { 
  Sparkles, 
  Zap, 
  Code2, 
  Smartphone, 
  Download, 
  Users,
  ArrowRight,
  Play,
  Star
} from 'lucide-react';

const features = [
  {
    icon: Sparkles,
    title: 'AI-Powered Generation',
    description: 'Describe your UI in natural language and watch as AI generates beautiful Flutter code instantly.',
  },
  {
    icon: Code2,
    title: 'Production-Ready Code',
    description: 'Get clean, well-structured Dart code that follows Flutter best practices and Material Design.',
  },
  {
    icon: Smartphone,
    title: 'Live Device Preview',
    description: 'See your generated UI in real-time with our interactive device simulator and hot reload.',
  },
  {
    icon: Zap,
    title: 'Multiple Variants',
    description: 'Generate multiple design variants to choose from and iterate on your perfect UI.',
  },
  {
    icon: Download,
    title: 'One-Click Export',
    description: 'Export your complete Flutter project as a ZIP, ready to open in your favorite IDE.',
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'Invite team members, share projects, and build Flutter apps together.',
  },
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="container max-w-7xl mx-auto h-16 flex items-center justify-between px-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="font-bold text-xl">FlutterAI</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-6">
            <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Features
            </a>
            <a href="#pricing" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Pricing
            </a>
            <a href="#docs" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Docs
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <Link to="/dashboard">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link to="/dashboard">
              <Button className="gap-2">
                Get Started
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-24 relative overflow-hidden">
        {/* Background Decoration */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl" />
        </div>

        <div className="container max-w-7xl mx-auto px-4 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm mb-8">
            <Sparkles className="w-4 h-4" />
            <span>Now with GPT-5 powered generation</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Build Flutter UIs
            <br />
            <span className="text-primary">with AI</span>
          </h1>

          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            Transform your ideas into production-ready Flutter code. Just describe what you want, 
            and our AI will generate beautiful, responsive UIs in seconds.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link to="/dashboard">
              <Button size="lg" className="gap-2 px-8">
                <Zap className="w-5 h-5" />
                Start Building Free
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="gap-2 px-8">
              <Play className="w-5 h-5" />
              Watch Demo
            </Button>
          </div>

          {/* Hero Visual */}
          <div className="relative max-w-5xl mx-auto">
            <div className="aspect-video rounded-2xl bg-card border border-border shadow-2xl overflow-hidden">
              <div className="h-10 bg-muted/50 border-b border-border flex items-center px-4 gap-2">
                <div className="w-3 h-3 rounded-full bg-destructive/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-green-500/50" />
              </div>
              <div className="flex h-[calc(100%-2.5rem)]">
                {/* File Explorer Mock */}
                <div className="w-48 border-r border-border p-3 hidden md:block">
                  <div className="space-y-1">
                    {['lib/', '  main.dart', '  widgets/', 'pubspec.yaml'].map((item, i) => (
                      <div key={i} className="text-xs text-muted-foreground py-1 px-2 rounded hover:bg-accent/50">
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
                {/* Code Editor Mock */}
                <div className="flex-1 p-4 font-mono text-xs text-left bg-card">
                  <div className="text-blue-500">import</div>
                  <div className="text-muted-foreground">'package:flutter/material.dart';</div>
                  <br />
                  <div className="text-purple-500">class</div>
                  <div className="text-foreground"> MyApp <span className="text-purple-500">extends</span> StatelessWidget {'{'}</div>
                  <div className="pl-4 text-muted-foreground">// AI generated code...</div>
                </div>
                {/* Preview Mock */}
                <div className="w-64 border-l border-border p-4 hidden lg:flex items-center justify-center">
                  <div className="w-32 h-56 bg-foreground rounded-2xl p-1">
                    <div className="w-full h-full bg-card rounded-xl flex items-center justify-center">
                      <Smartphone className="w-8 h-8 text-muted-foreground" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-muted/30">
        <div className="container max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Everything you need to build Flutter apps
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              From ideation to export, FlutterAI streamlines your entire UI development workflow.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <div 
                key={i}
                className="p-6 rounded-2xl bg-card border border-border hover:border-primary/50 hover:shadow-lg transition-all"
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-24">
        <div className="container max-w-7xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-1 mb-4">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="w-6 h-6 fill-yellow-500 text-yellow-500" />
            ))}
          </div>
          <p className="text-2xl font-medium mb-2">
            "FlutterAI saved me hours of UI development time."
          </p>
          <p className="text-muted-foreground">
            — Flutter Developer, 10,000+ users worldwide
          </p>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-primary/5">
        <div className="container max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to supercharge your Flutter workflow?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Join thousands of developers building beautiful Flutter apps with AI.
          </p>
          <Link to="/dashboard">
            <Button size="lg" className="gap-2 px-8">
              <Sparkles className="w-5 h-5" />
              Start Building for Free
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12">
        <div className="container max-w-7xl mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded bg-primary flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-primary-foreground" />
              </div>
              <span className="font-semibold">FlutterAI Playground</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2024 FlutterAI. Built with ❤️ for Flutter developers.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
