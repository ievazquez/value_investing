import React, { useState } from 'react';

function ExpandableSection({ title, children, defaultExpanded = false }) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <div className="expandable-section">
      <div
        className="expandable-header"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <h3 className="expandable-title">{title}</h3>
        <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
          ▼
        </span>
      </div>
      {isExpanded && (
        <div className="expandable-content">
          {children}
        </div>
      )}
    </div>
  );
}

export default ExpandableSection;
