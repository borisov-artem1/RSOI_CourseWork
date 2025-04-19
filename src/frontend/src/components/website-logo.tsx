import React from 'react'
import MenuBookIcon from '@mui/icons-material/MenuBook';
import Text from './text';

interface WebsiteLogoProps {
  size: "mini" | "little" | "medium" | "high" | "large";
}

export function WebsiteLogo({size}: WebsiteLogoProps) {
  return (
    <a 
      href="/"
      className="flex flex-row gap-x-2 border justify-center bg-my-secondary-color p-1 rounded-md"
    >
      <Text size={size}
        className={`text-my-third-color`}
      >
        LibraREALLY
      </Text>
      <MenuBookIcon
        style={{fontSize: `var(--my-${size}-size)`, lineHeight: `var(--my-${size}-height)`}}
        className="text-my-third-color" 
      />
    </a>
  )
}
