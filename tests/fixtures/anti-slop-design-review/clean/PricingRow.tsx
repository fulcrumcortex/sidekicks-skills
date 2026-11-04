type Props = { plan: string; price: number };

export function PricingRow({ plan, price }: Props) {
  return (
    <article className="grid grid-cols-[1fr_auto] items-baseline gap-4 border-t border-ink/15 py-6">
      <h3 className="font-display text-[length:var(--text-display)] tracking-tight">{plan}</h3>
      <p className="tabular-nums text-ink-muted">${price} a month, plus GST</p>
    </article>
  );
}
