import { LogSeverity } from "@/types/log";
import { ReactNode, useMemo, useRef } from "react";
import { CSSTransition } from "react-transition-group";

type ChipProps = {
  className?: string;
  children?: ReactNode | ReactNode[];
  in?: boolean;
  onClick?: () => void;
};

export default function Chip({
  className,
  children,
  in: inProp = true,
  onClick,
}: ChipProps) {
  const nodeRef = useRef(null);

  return (
    <CSSTransition
      in={inProp}
      nodeRef={nodeRef}
      timeout={500}
      classNames={{
        enter: "opacity-0",
        enterActive: "opacity-100 transition-opacity duration-500 ease-in-out",
        exit: "opacity-100",
        exitActive: "opacity-0 transition-opacity duration-500 ease-in-out",
      }}
      unmountOnExit
    >
      <div
        ref={nodeRef}
        className={`flex px-2 py-1.5 rounded-2xl items-center z-10 ${className}`}
        onClick={onClick}
      >
        {children}
      </div>
    </CSSTransition>
  );
}

type LogChipProps = {
  severity: LogSeverity;
  onClickSeverity?: () => void;
};
export function LogChip({ severity, onClickSeverity }: LogChipProps) {
  const severityClassName = useMemo(() => {
    switch (severity) {
      case "info":
        return "text-primary/60 bg-secondary hover:bg-secondary/60";
      case "warning":
        return "text-warning-foreground bg-warning hover:bg-warning/80";
      case "error":
        return "text-destructive-foreground bg-destructive hover:bg-destructive/80";
    }
  }, [severity]);

  return (
    <div
      className={`py-[1px] px-1 capitalize text-xs rounded-md ${onClickSeverity ? "cursor-pointer" : ""} ${severityClassName}`}
      onClick={(e) => {
        e.stopPropagation();

        if (onClickSeverity) {
          onClickSeverity();
        }
      }}
    >
      {severity}
    </div>
  );
}
