from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter



# ----------------------------
# PDF Generator
# ----------------------------

def create_pdf(
    filename,
    subject,
    topic,
    mcqs
):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )


    styles = getSampleStyleSheet()


    story = []


    # Title

    story.append(
        Paragraph(
            "🤖 QuizMind AI - MCQ Report",
            styles["Title"]
        )
    )


    story.append(
        Spacer(1,20)
    )


    # Details

    story.append(
        Paragraph(
            f"<b>Subject:</b> {subject}",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Topic:</b> {topic}",
            styles["Normal"]
        )
    )


    story.append(
        Spacer(1,20)
    )



    # Questions

    for index, mcq in enumerate(mcqs,1):


        story.append(

            Paragraph(

                f"Q{index}. {mcq.get('question','')}",

                styles["Heading3"]

            )

        )


        story.append(
            Spacer(1,8)
        )


        # Options

        for option in mcq.get("options", []):

            story.append(

                Paragraph(

                    f"• {option}",

                    styles["Normal"]

                )

            )


        story.append(
            Spacer(1,8)
        )


        # Answer

        story.append(

            Paragraph(

                f"<b>Correct Answer:</b> {mcq.get('answer','')}",

                styles["Normal"]

            )

        )


        story.append(
            Spacer(1,5)
        )


        # Explanation

        story.append(

            Paragraph(

                f"<b>Explanation:</b> {mcq.get('explanation','')}",

                styles["Normal"]

            )

        )


        story.append(
            Spacer(1,20)
        )


        # Page break after every 5 questions

        if index % 5 == 0 and index != len(mcqs):

            story.append(
                PageBreak()
            )


    # Build PDF

    doc.build(story)