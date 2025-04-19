import React, { Children } from 'react'
import Text from './text';

interface MultilineTextProps {
  size: "mini" | "little" | "medium" | "high" | "large";
  className?: string;
}

export default function MultilineText({size, className, children}: React.PropsWithChildren<MultilineTextProps>) {
  const chlidrenArray = Children.toArray(children);
  return (
    <div className={`flex flex-col ${className}`}>
      {chlidrenArray.map((c, index) => 
        <Text
          key={index}
          size={size}
        >
          {c}
        </Text>
      )}
    </div>
  )
}
