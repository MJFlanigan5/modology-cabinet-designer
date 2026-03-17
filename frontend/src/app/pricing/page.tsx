'use client';

import React, { useState } from 'react';
import { Check, Zap, Building2, Crown } from 'lucide-react';
import { SUBSCRIPTION_PLANS, createCheckoutSession } from '@/lib/stripe';
import type { PlanId } from '@/lib/stripe';

interface PricingCardProps {
  planId: PlanId;
  plan: typeof SUBSCRIPTION_PLANS[PlanId];
  onSelect: (planId: PlanId) => void;
  isLoading?: boolean;
  currentPlan?: PlanId;
}

const planIcons: Record<PlanId, React.ReactNode> = {
  free: <Zap className="w-6 h-6" />,
  hobbyist: <Check className="w-6 h-6" />,
  pro: <Building2 className="w-6 h-6" />,
  shop: <Crown className="w-6 h-6" />,
};

const planColors: Record<PlanId, string> = {
  free: 'border-gray-300 bg-white',
  hobbyist: 'border-blue-500 bg-blue-50',
  pro: 'border-purple-500 bg-purple-50 ring-2 ring-purple-500',
  shop: 'border-amber-500 bg-gradient-to-b from-amber-50 to-orange-50',
};

const buttonColors: Record<PlanId, string> = {
  free: 'bg-gray-600 hover:bg-gray-700',
  hobbyist: 'bg-blue-600 hover:bg-blue-700',
  pro: 'bg-purple-600 hover:bg-purple-700',
  shop: 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700',
};

function PricingCard({ planId, plan, onSelect, isLoading, currentPlan }: PricingCardProps) {
  const isCurrent = currentPlan === planId;
  const isPopular = planId === 'pro';
  
  return (
    <div
      className={`relative rounded-2xl border-2 p-6 ${planColors[planId]} ${
        isPopular ? 'scale-105' : ''
      }`}
    >
      {isPopular && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-purple-600 px-4 py-1 text-sm font-semibold text-white">
          Most Popular
        </div>
      )}
      
      <div className="flex items-center gap-3 mb-4">
        <div className={`p-2 rounded-lg ${planId === 'pro' ? 'bg-purple-100' : 'bg-gray-100'}`}>
          {planIcons[planId]}
        </div>
        <h3 className="text-xl font-bold">{plan.name}</h3>
      </div>
      
      <div className="mb-6">
        <span className="text-4xl font-bold">${plan.price}</span>
        {plan.price > 0 && <span className="text-gray-500">/month</span>}
      </div>
      
      <ul className="space-y-3 mb-6">
        {plan.features.map((feature, index) => (
          <li key={index} className="flex items-start gap-2">
            <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            <span className="text-sm">{feature}</span>
          </li>
        ))}
      </ul>
      
      <button
        onClick={() => onSelect(planId)}
        disabled={isLoading || isCurrent}
        className={`w-full py-3 rounded-lg font-semibold text-white transition-colors ${
          isCurrent
            ? 'bg-gray-400 cursor-not-allowed'
            : buttonColors[planId]
        } ${isLoading ? 'opacity-50 cursor-wait' : ''}`}
      >
        {isLoading ? 'Processing...' : isCurrent ? 'Current Plan' : plan.price === 0 ? 'Get Started' : 'Subscribe'}
      </button>
    </div>
  );
}

export default function PricingPage() {
  const [loading, setLoading] = useState<PlanId | null>(null);
  const [currentPlan, setCurrentPlan] = useState<PlanId>('free');
  
  const handleSelectPlan = async (planId: PlanId) => {
    if (planId === 'free') {
      // Handle free plan signup
      window.location.href = '/signup';
      return;
    }
    
    setLoading(planId);
    
    try {
      const plan = SUBSCRIPTION_PLANS[planId];
      const { url } = await createCheckoutSession(
        plan.priceId!,
        `${window.location.origin}/dashboard?success=true`,
        `${window.location.origin}/pricing?canceled=true`
      );
      
      window.location.href = url;
    } catch (error) {
      console.error('Failed to create checkout session:', error);
      alert('Failed to start checkout. Please try again.');
    } finally {
      setLoading(null);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50 py-16 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Choose Your Plan</h1>
          <p className="text-xl text-gray-600">
            Start free, upgrade when you need more features
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {(Object.entries(SUBSCRIPTION_PLANS) as [PlanId, typeof SUBSCRIPTION_PLANS[PlanId]][]).map(
            ([planId, plan]) => (
              <PricingCard
                key={planId}
                planId={planId}
                plan={plan}
                onSelect={handleSelectPlan}
                isLoading={loading === planId}
                currentPlan={currentPlan}
              />
            )
          )}
        </div>
        
        <div className="mt-12 text-center text-gray-500 text-sm">
          <p>All plans include: SSL security, automatic backups, 99.9% uptime SLA</p>
          <p className="mt-2">Questions? Contact us at support@modologystudios.com</p>
        </div>
      </div>
    </div>
  );
}
