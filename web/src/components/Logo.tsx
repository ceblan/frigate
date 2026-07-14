import { cn } from "@/lib/utils";

type LogoProps = {
  className?: string;
};
export default function Logo({ className }: LogoProps) {
  return (
    <img
      src="/images/branding/favicon.svg"
      alt="BIS-IA"
      className={cn("object-contain", className)}
    />
  );
}
