import React from 'react';

interface IconProps {
  size?: 'small' | 'medium' | 'large';
  color?: string;
  className?: string;
}

const sizeMap = {
  small: 16,
  medium: 24,
  large: 32,
};

export const HomeIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => {
  const px = sizeMap[size];
  return (
    <svg width={px} height={px} viewBox="0 0 24 24" fill="none" className={className}>
      <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill={color} />
    </svg>
  );
};

export const DatabaseIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => {
  const px = sizeMap[size];
  return (
    <svg width={px} height={px} viewBox="0 0 24 24" fill="none" className={className}>
      <path d="M12 3C7.58 3 4 4.79 4 7s3.58 4 8 4 8-1.79 8-4-3.58-4-8-4zm8 6c0 2.21-3.58 4-8 4s-8-1.79-8-4v3c0 2.21 3.58 4 8 4s8-1.79 8-4V9zm0 5c0 2.21-3.58 4-8 4s-8-1.79-8-4v3c0 2.21 3.58 4 8 4s8-1.79 8-4v-3z" fill={color} />
    </svg>
  );
};

export const ChatIcon: React.FC<IconProps> = ({ size = 'medium', color = 'currentColor', className }) => {
  const px = sizeMap[size];
  return (
    <svg width={px} height={px} viewBox="0 0 24 24" fill="none" className={className}>
      <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" fill={color} />
    </svg>
  );
};
