import { CONTRIBUTE_REPO_URL } from "@/lib/site";

/** Issue form in the public repo (.github/ISSUE_TEMPLATE/question-problem.yml); its field ids are prefilled below. */
export const QUESTION_PROBLEM_FORM = "question-problem.yml";

/** The question's file in the public repo, e.g. questions/en/az-104/question-025.md. */
export function questionFileUrl(cert: string, questionId: string): string {
  const number = questionId.startsWith(`${cert}-`) ? questionId.slice(cert.length + 1) : questionId;
  return `${CONTRIBUTE_REPO_URL}/blob/main/questions/en/${cert}/question-${number}.md`;
}

/** "Improve" link: GitHub's web editor for the question's file; GitHub offers to fork, then to open a pull request. */
export function questionEditUrl(cert: string, questionId: string): string {
  return questionFileUrl(cert, questionId).replace("/blob/main/", "/edit/main/");
}

/**
 * "Report a problem" link: opens the issue form with the question id and file filled in, so a reader only says what's
 * wrong. GitHub prefills issue-form fields from query parameters named after the field ids.
 */
export function questionReportUrl(cert: string, questionId: string, title: string): string {
  const params = new URLSearchParams({
    template: QUESTION_PROBLEM_FORM,
    title,
    "question-id": questionId,
    "question-file": questionFileUrl(cert, questionId),
  });
  return `${CONTRIBUTE_REPO_URL}/issues/new?${params.toString()}`;
}
