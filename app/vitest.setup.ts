import { afterEach } from "vitest";

// Unmount what each test rendered. Without this, @testing-library/react keeps earlier renders in the document
// (vitest globals are off, so RTL's auto-cleanup never registers) and later queries find duplicates.
afterEach(async () => {
  if (typeof document === "undefined") return; // node-environment tests render nothing
  const { cleanup } = await import("@testing-library/react");
  cleanup();
});
