/* ==========================================================================
   Site map — the ONE place that lists notes and projects for navigation.
   It feeds: the sidebar sub-menu, the "previous / next" links, the counts and
   the "← Back to …" label. Paths are relative to the site root.

   Adding a note or project:  add a line here, then add its row to the list page
   (notes.html / projects.html). See README.md → "Adding a field note".
   Order matters: newest first within a group.
   ========================================================================== */
window.SITE = {
  pages: {
    'index.html': 'Home',
    'projects.html': 'Projects',
    'notes.html': 'Notes',
    'now.html': 'Now',
    'about.html': 'About'
  },
  groups: [
    { id: 'travel', title: 'Travel' },
    { id: 'cricket-family', title: 'Cricket and family' },
    { id: 'engineering', title: 'Engineering' }
  ],
  projects: [
    { href: 'projects/nihiramusic.html', title: 'nihiramusic.in', status: 'Live' },
    { href: 'projects/cricketiq.html', title: 'CricketIQ', status: 'Live' },
    { href: 'household-finance-tracker.html', title: 'Household Finance Tracker', status: 'Live' },
    { href: 'projects/visaflow.html', title: 'VisaFlow', status: 'Prototype' },
    { href: 'projects/famdeck.html', title: 'FamDeck', status: 'In progress' },
    { href: 'projects/cad.html', title: 'Notes on engineering software', status: 'Writing topic' }
  ],
  notes: [
    { href: 'notes/family-first.html', title: 'Husband and dad, before everything', group: 'cricket-family' },
    { href: 'notes/cricket-analyst.html', title: 'From the crease to the analyst’s laptop', group: 'cricket-family' },
    { href: 'notes/built-on-curves.html', title: 'A career built on curves', group: 'engineering' },
    { href: 'notes/small-steps.html', title: 'Small steps you can review', group: 'engineering' },
    { href: 'notes/self-hosted-fonts.html', title: 'Self-hosting web fonts on a static site', group: 'engineering' },
    { href: 'notes/boring-technology.html', title: 'The case for boring, reliable technology', group: 'engineering' },
    /* ext = essay that lives elsewhere (Substack). Counted, but not shown in the sidebar. */
    { ext: 'https://get2abhijit.substack.com/p/i-built-my-wife-a-website-in-4-days', title: 'I built my wife a website in 4 days. Here’s why', group: 'engineering' }
  ]
};
