interface ProgressBarProps {
  current: number;
  total: number;
  level?: number;
  className?: string;
}

const ProgressBar = ({ current, total, level, className = "" }: ProgressBarProps) => {
  const percentage = Math.min((current / total) * 100, 100);

  return (
    <div className={`space-y-2 ${className}`}>
      {level && (
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-muted-foreground">
            Level {level}
          </span>
          <span className="text-sm text-muted-foreground">
            {current}/{total}
          </span>
        </div>
      )}
      
      <div className="relative">
        <div className="h-3 bg-progress-bg rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-primary to-primary-glow transition-all duration-700 ease-out rounded-full"
            style={{ width: `${percentage}%` }}
          />
        </div>
        
        {/* Glow effect */}
        <div 
          className="absolute top-0 h-full bg-gradient-to-r from-primary-glow to-primary opacity-50 blur-sm transition-all duration-700 ease-out rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;