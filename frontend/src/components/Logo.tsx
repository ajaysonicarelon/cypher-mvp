import React from 'react';

interface LogoProps {
  collapsed?: boolean;
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({ collapsed = false, className }) => {
  return (
    <div className={className} style={{ display: 'flex', alignItems: 'center', padding: '8px' }}>
      {collapsed ? (
        <img 
          src={`${process.env.PUBLIC_URL}/carelon-symbol.png`}
          alt="Carelon Symbol" 
          style={{ width: '40px', height: '40px', objectFit: 'contain' }}
        />
      ) : (
        <img 
          src={`${process.env.PUBLIC_URL}/carelon-logo.png`}
          alt="Carelon Logo" 
          style={{ height: '40px', width: 'auto', maxWidth: '140px', objectFit: 'contain' }}
        />
      )}
    </div>
  );
};
