import { useState, useEffect } from 'react';

export function NotificationContainer({ notifications, onRemove }) {
  if (notifications.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm">
      {notifications.map((notification) => (
        <NotificationItem
          key={notification.id}
          notification={notification}
          onRemove={onRemove}
        />
      ))}
    </div>
  );
}

function NotificationItem({ notification, onRemove }) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Trigger entrada animation
    setTimeout(() => setIsVisible(true), 10);
  }, []);

  const handleRemove = () => {
    setIsVisible(false);
    setTimeout(() => onRemove(notification.id), 300);
  };

  const getIcon = () => {
    switch (notification.type) {
      case 'success': return '✅';
      case 'error': return '❌';
      case 'warning': return '⚠️';
      default: return 'ℹ️';
    }
  };

  const getStyles = () => {
    const baseStyles = 'border shadow-lg backdrop-blur-sm';
    switch (notification.type) {
      case 'success':
        return `${baseStyles} bg-green-900/80 border-green-500/50 text-green-100`;
      case 'error':
        return `${baseStyles} bg-red-900/80 border-red-500/50 text-red-100`;
      case 'warning':
        return `${baseStyles} bg-yellow-900/80 border-yellow-500/50 text-yellow-100`;
      default:
        return `${baseStyles} bg-blue-900/80 border-blue-500/50 text-blue-100`;
    }
  };

  return (
    <div
      className={`
        ${getStyles()}
        rounded-lg p-4 transition-all duration-300 transform
        ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
      `}
    >
      <div className="flex items-start gap-3">
        <span className="text-lg flex-shrink-0">{getIcon()}</span>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium break-words">{notification.message}</p>
        </div>
        <button
          onClick={handleRemove}
          className="text-current opacity-70 hover:opacity-100 transition-opacity flex-shrink-0"
        >
          ✕
        </button>
      </div>
    </div>
  );
}