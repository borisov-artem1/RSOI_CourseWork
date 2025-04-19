import { PropsWithChildren } from 'react'

interface TextProps {
  size: "mini" | "little" | "medium" | "high" | "large";
  className?: string;
}

export default function Text({size, className, children}: PropsWithChildren<TextProps>) {
  return (
    <div
      className={className}
      style={{fontSize: `var(--my-${size}-size)`, lineHeight: `var(--my-${size}-height)`}}>
      {children}
    </div>
  )
}
