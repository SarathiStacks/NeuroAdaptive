import { useEffect } from "react";
import confetti from "canvas-confetti";

export default function Confetti() {
  useEffect(() => {
    confetti({ particleCount: 80, spread: 60 });
  }, []);
  return null;
}
