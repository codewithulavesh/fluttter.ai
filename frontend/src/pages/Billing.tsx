import { AppHeader } from '@/components/layout/AppHeader';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  CreditCard, 
  Zap, 
  Check, 
  Sparkles,
  TrendingUp,
  Calendar
} from 'lucide-react';
import { cn } from '@/lib/utils';

const plans = [
  {
    id: 'free',
    name: 'Free',
    price: '$0',
    period: 'forever',
    description: 'Perfect for trying out FlutterAI',
    features: [
      '3 projects',
      '100 generations/month',
      'Community support',
      'Export to ZIP',
    ],
    current: true,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$19',
    period: '/month',
    description: 'For serious Flutter developers',
    features: [
      'Unlimited projects',
      '1,000 generations/month',
      'Priority support',
      'Team collaboration',
      'Custom templates',
    ],
    popular: true,
  },
  {
    id: 'team',
    name: 'Team',
    price: '$49',
    period: '/month',
    description: 'For teams building together',
    features: [
      'Everything in Pro',
      '5,000 generations/month',
      '10 team members',
      'Admin dashboard',
      'API access',
      'SSO integration',
    ],
  },
];

export default function Billing() {
  return (
    <div className="min-h-screen bg-background">
      <AppHeader />

      <main className="container max-w-6xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Billing</h1>
          <p className="text-muted-foreground">
            Manage your subscription and usage
          </p>
        </div>

        {/* Current Usage */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Current Plan
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <span className="text-2xl font-bold">Free</span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Generations Used
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold">24</span>
                  <span className="text-sm text-muted-foreground">/ 100</span>
                </div>
                <Progress value={24} className="h-2" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                Billing Cycle
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-muted-foreground" />
                <span className="text-lg font-medium">Resets in 22 days</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Usage History */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Usage This Month
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-32 flex items-end gap-2">
              {[12, 8, 15, 6, 10, 18, 24].map((value, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-2">
                  <div 
                    className="w-full bg-primary/20 rounded-t"
                    style={{ height: `${(value / 24) * 100}%` }}
                  >
                    <div 
                      className="w-full bg-primary rounded-t transition-all"
                      style={{ height: `${(value / 24) * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][i]}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Pricing Plans */}
        <h2 className="text-xl font-semibold mb-4">Plans</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <Card 
              key={plan.id}
              className={cn(
                'relative',
                plan.popular && 'border-primary shadow-lg'
              )}
            >
              {plan.popular && (
                <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
                  Most Popular
                </Badge>
              )}
              
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {plan.name}
                  {plan.current && (
                    <Badge variant="secondary">Current</Badge>
                  )}
                </CardTitle>
                <CardDescription>{plan.description}</CardDescription>
              </CardHeader>

              <CardContent>
                <div className="mb-6">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="text-muted-foreground">{plan.period}</span>
                </div>

                <ul className="space-y-3">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm">
                      <Check className="w-4 h-4 text-primary" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </CardContent>

              <CardFooter>
                <Button 
                  className="w-full gap-2"
                  variant={plan.current ? 'outline' : plan.popular ? 'default' : 'secondary'}
                  disabled={plan.current}
                >
                  {plan.current ? (
                    'Current Plan'
                  ) : (
                    <>
                      <Zap className="w-4 h-4" />
                      Upgrade
                    </>
                  )}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Payment Method */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CreditCard className="w-5 h-5" />
              Payment Method
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              No payment method on file. Add one to upgrade your plan.
            </p>
          </CardContent>
          <CardFooter>
            <Button variant="outline">Add Payment Method</Button>
          </CardFooter>
        </Card>
      </main>
    </div>
  );
}
