# Profile design notes

Research checked on September 21, 2026. This is a curated shortlist of useful approaches, not an objective ranking of GitHub profiles.

## Direction

A personal engineering fieldbook: charcoal, warm paper, mint accents, generous spacing, and specific work. The theme-aware animated hero establishes the visual identity; the text explains what Tejas builds and links to evidence. Project stories stay readable at a glance, with expandable engineering notes for readers who want more.

The profile should feel personal and explorable. Claims, roles, metrics, awards, and links must remain verifiable. Authored work and team contributions should be described accurately.

## Research shortlist

| Original repository | Useful idea | Decision |
| --- | --- | --- |
| [simonw/simonw](https://github.com/simonw/simonw) | Dated releases and writing make current work visible. | Show useful evidence of ongoing work, with dates and destinations. |
| [anuraghazra/anuraghazra](https://github.com/anuraghazra/anuraghazra) | A custom header, short identity, and linked projects form a clear introduction. | Give original art and actual work the strongest placement. |
| [DenverCoder1/DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) | Native disclosure sections organize projects, contributions, tools, and statistics. | Use expandable project stories and explicit contribution attribution. |
| [sindresorhus/sindresorhus](https://github.com/sindresorhus/sindresorhus) | Consistent art direction and very few destinations create a memorable personality. | Keep one coherent visual language and clear next steps. |
| [timburgan/timburgan](https://github.com/timburgan/timburgan) | Chess moves open prefilled issues; Actions update the shared board. | Learn from real interaction, but avoid adding an unrelated game and its maintenance. |
| [Platane/snk](https://github.com/Platane/snk) | Contribution data becomes an animated SVG with light/dark variants. | Let one contribution feature provide movement and evidence; do not stack competing widgets. |
| [lowlighter/metrics](https://github.com/lowlighter/metrics) | Configurable plugins turn GitHub activity into visual artifacts. | Keep the public-data feature focused rather than building a large dashboard. |
| [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | Repository-stored SVGs can be generated with Actions; the shared endpoint is explicitly best-effort. | Generate and commit the profile's own assets instead of depending on a shared rendering endpoint. |
| [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | Controlled SVG motion can add personality to a header. | Use restrained local animation while keeping the identity readable without waiting. |
| [kyechan99/capsule-render](https://github.com/kyechan99/capsule-render) | Headers can combine shape, color, typography, and animation. | Create a bespoke fieldbook hero rather than a stock banner. |
| [gautamkrishnar/blog-post-workflow](https://github.com/gautamkrishnar/blog-post-workflow) | Marked README sections can update from an established RSS feed. | Add feeds only when there is a verified, regularly maintained source. |
| [antonkomarev/github-profile-views-counter](https://github.com/antonkomarev/github-profile-views-counter) | The counter measures page/proxy requests, not unique visitors. | Omit visitor counters; they do not establish the quality of the work. |

## Interaction that works on GitHub

- **Expandable stories:** GitHub supports `<details>` and `<summary>`, including Markdown content inside the disclosure. These are actual visitor-controlled interactions. [Official documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- **Theme-aware images:** `<picture>` and `prefers-color-scheme` sources select light/dark artwork, with an `<img>` fallback and descriptive alt text. [GitHub profile-writing quickstart](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)
- **Navigation:** ordinary links, linked images, and heading links provide clear paths to projects, demos, and further detail. [GitHub writing syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- **No embedded application:** GitHub sanitizes README HTML, including scripts and inline styles. Client-side tabs, editable terminals, and JavaScript games cannot run in the README. [GitHub rendering pipeline](https://github.com/github/markup)
- **SVG is an image here:** JavaScript is disabled in SVG image contexts, and external resources cannot normally load. Keep artwork self-contained and wrap the whole image in a link when needed. Animation is presentation, not a playable control. [MDN SVG image restrictions](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)

## Assets and updates

Keep the hero and contribution artwork in the repository. This avoids a rendering-service request for every visitor and keeps a useful image available when a data refresh fails. This choice follows the reliability tradeoff documented by [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats#deploy-on-your-own-recommended).

Use one daily contribution card generated by a small Python standard-library script from public data. Label its coverage and snapshot date. Contribution counts describe recorded activity; they are not a score for skill, work quality, or overall productivity. Retain the project stories as the main evidence.

A failed refresh must preserve the last successful artifact and report failure in the workflow. It must not replace valid data with zeroes or advance the snapshot date. Commit generated changes only when they differ; provide manual dispatch for recovery.

Scheduled workflows run on the default branch and can be delayed. GitHub can disable public-repository schedules after 60 days without repository activity, so a daily schedule is not a freshness guarantee. The displayed snapshot date and last successful artifact remain useful when refreshes stop. [GitHub schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

Pin adopted Actions to verified full commit SHAs and update those pins deliberately. [GitHub versioning guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions#using-shas)

## Maintaining this profile

The README is hand-written. Original illustrations are generated from `scripts/render_artwork.py`; activity graphics and provenance come from `scripts/update_activity.py`. Both generators use Python's standard library. No personal access token or external image-rendering service is needed for activity refreshes.

```sh
python3 scripts/render_artwork.py        # Rebuild original artwork, offline
python3 scripts/update_activity.py       # Refresh from public GitHub sources
python3 scripts/test_activity.py         # Data integrity and failure handling
python3 scripts/update_activity.py --check  # Verify stored data and graphics, offline
python3 scripts/preview.py --serve       # GitHub-rendered local preview
```

The preview requires an authenticated GitHub CLI (`gh`) to call the Markdown rendering API. It binds only to localhost; open `http://127.0.0.1:8766/dark.html` or `/light.html`. Preview files stay in the Git metadata directory, outside the published tree. The wrapper supplies GitHub styles and heading anchors; the final hosted profile should also be checked after publication.

The activity workflow validates pull requests and generator changes without write access. Daily and manually dispatched refreshes use the built-in GitHub Actions token with repository-content write access and commit only the five generated activity files. Scheduling becomes active when the workflow reaches the default branch, subject to repository Actions settings and branch rules. A custom PAT is not required.

Project interfaces are linked separately from their source code. RelayPass is explicitly a simulation; a working frontend link does not establish that every backend integration in any featured project is currently operational. Existing career history and established impact claims are retained with their original personal-versus-team attribution.

Live browser review on September 21, 2026 found RelayPass's hosted page loading successfully but its demo initialization returning HTTP 503 on two attempts. The profile therefore links to the verified architecture and source, and omits the demo link until the application is repaired and rechecked. ACS and ModelMind's advertised demo URLs also returned 404 and are omitted.
