# Profile design notes

Original profile research checked on September 21, 2026. Identity, published portfolio content, and the blue visual revision checked on October 7, 2026; the branching hero, motion, and promotion cards were revised the same day. The research shortlist is a curated set of useful approaches, not an objective ranking of GitHub profiles.

## Direction

A personal engineering fieldbook in blue: midnight navy, cobalt, ice blue, and pale blue surfaces. Light/dark and narrow-screen variants share the same visual language.

The hero restores the branching composition Tejass preferred from the first fieldbook revision (September 2026), redrawn in the blue palette. One source routes a signal to three nodes, INTERFACES, INTELLIGENCE, and SYSTEMS, beside his name. It summarizes the range of the work in one image instead of a list of technologies. The water theme now lives in the Open Water card, next to the portfolio it describes.

The introduction answers who Tejass is, what he builds, and how he works before the project list. Current engineering, prior leadership, research, personal interests, and contact paths sit alongside the code. Project stories and longer career notes remain expandable so readers can choose their level of detail.

Two linked promotion cards give the profile's main destinations visual weight: Anticipy, the product Tejass is helping build, opens *Now*; Open Water, his portfolio, opens its entry in *The lab*. The top link row leads with the same two destinations, followed by resume, LinkedIn, and email.

The profile should feel personal and explorable. Claims, roles, metrics, awards, and links must remain verifiable. Authored work and team contributions should be described accurately.

## Motion

Motion decorates the images. It never carries information that is missing from the static frame or the text.

- **Signal routes:** in the hero, short highlights travel along the branch paths from the source to each node.
- **Node pulses:** the source and nodes brighten gently on slow, staggered cycles.
- **Waveform:** the Anticipy card uses a low, slow waveform, a nod to spoken intentions.
- **Drifting waves:** the Open Water card's wave lines drift at a calm pace.

Rules for every animated asset:

- Define the animation inside the self-contained SVG: no scripts, web fonts, or remote resources.
- Keep cycles slow and low in amplitude, with no flashing. Text stays still and readable.
- Include a `prefers-reduced-motion: reduce` rule inside the SVG, and select a generated `*-still-*.svg` through host-page `<picture>` sources when reduced motion is enabled. This makes the still composition reliable even in browsers that do not forward the preference into embedded SVG images. Still variants contain no keyframes or animation declarations.
- Design the static frame to work on its own; some clients display SVG images without animation.

Interaction comes from what GitHub supports: linked cards, text links, heading anchors, and `<details>` disclosures. The animation is not a control.

## Promotion cards

- **Anticipy** sits immediately below *Now* and links to [anticipy.ai](https://www.anticipy.ai/). Its copy describes an AI wearable being built to turn spoken intentions into actions with the person's approval. It does not present Anticipy as complete, launched, or generally available, and adds no user, waitlist, or launch-date claims.
- **Open Water** sits immediately below its heading in *The lab* and links to the [portfolio](https://tejass-kaushik.vercel.app/). Its copy is limited to features the portfolio publishes.
- Each card is one `<a>` around a `<picture>` with reduced-motion still sources first (dark narrow, narrow, dark, light), followed by the animated sources (dark narrow, narrow, dark) and the light `<img>` fallback at `width="100%"`, lazily loaded. Because the whole image is the link, its alt text names the destination and summarizes the card. Nearby text links remain for readers who skip images.
- The copy is warm and direct, and follows the same rule as the rest of the profile: claims stay verifiable and accurately attributed.

## October 2026 content sources

- [Published portfolio](https://tejass-kaushik.vercel.app/) and [resume](https://tejass-kaushik.vercel.app/resume): current display name **Tejass Kaushik**, public email **tejas.kaushik@outlook.com**, Founding Software Engineer at Anticipation Labs, former Stellar CTO, Western Computer Science and Ivey AEO, working approach, and the personal water/boat interests. AEO is a status, not an HBA degree.
- [Anticipy case study](https://tejass-kaushik.vercel.app/case-studies/anticipy): connected-app reliability, private AI workflow prototypes, personal phone/hardware observations, and AI-assisted implementation under Tejass's direction. The Fellowship is coming soon; the old claim that the complete experience had shipped was removed. Existing team foundations and bounded validation remain explicit.
- [Stellar case study](https://tejass-kaushik.vercel.app/case-studies/stellar-learning): IB Diploma question-generation and practice harnesses, plus AP question and lesson harness improvements. The 40,000+ learners figure belongs to the organization.
- [Research case study](https://tejass-kaushik.vercel.app/case-studies/global-health-research), linked to the final 2025 Youreka Canada Journal: coauthors, the 34-country study, and national first-place recognition of the team study. No clinical impact or causal result is claimed.
- Open Water and RelayPass retain the AI-assistance credit stated on the published portfolio. Existing project descriptions and earlier career history are retained, with prototype/simulation and campaign-versus-personal distinctions intact.
- Promotion destinations: [anticipy.ai](https://www.anticipy.ai/) and the [portfolio](https://tejass-kaushik.vercel.app/) returned HTTP 200 on October 7, 2026. Tejass reconfirmed the public email **tejas.kaushik@outlook.com** the same day; every `mailto:` link uses it.

These sources support public biography, not a fresh end-to-end test of every featured product. The October revision keeps the existing dated activity snapshot intact and changes only its rendering palette; future scheduled refreshes use the same blue colors.

## Research shortlist

| Original repository | Useful idea | Decision |
| --- | --- | --- |
| [simonw/simonw](https://github.com/simonw/simonw) | Dated releases and writing make current work visible. | Show useful evidence of ongoing work, with dates and destinations. |
| [anuraghazra/anuraghazra](https://github.com/anuraghazra/anuraghazra) | A custom header, short identity, and linked projects form a clear introduction. | Give original art and actual work the strongest placement. |
| [DenverCoder1/DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) | Native disclosure sections organize projects, contributions, tools, and statistics. | Use expandable project stories and explicit contribution attribution. |
| [sindresorhus/sindresorhus](https://github.com/sindresorhus/sindresorhus) | Consistent art direction and very few destinations create a memorable personality. | Keep one coherent visual language and clear next steps. |
| [timburgan/timburgan](https://github.com/timburgan/timburgan) | Chess moves open prefilled issues; Actions update the shared board. | Learn from real interaction, but avoid adding an unrelated game and its maintenance. |
| [Platane/snk](https://github.com/Platane/snk) | Contribution data becomes an animated SVG with light/dark variants. | Use one contribution feature as evidence; keep motion to a few restrained, original animations instead of stacking widgets. |
| [lowlighter/metrics](https://github.com/lowlighter/metrics) | Configurable plugins turn GitHub activity into visual artifacts. | Keep the public-data feature focused rather than building a large dashboard. |
| [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | Repository-stored SVGs can be generated with Actions; the shared endpoint is explicitly best-effort. | Generate and commit the profile's own assets instead of depending on a shared rendering endpoint. |
| [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | Controlled SVG motion can add personality to a header. | Use restrained local animation while keeping the identity readable without waiting. |
| [kyechan99/capsule-render](https://github.com/kyechan99/capsule-render) | Headers can combine shape, color, typography, and animation. | Create a bespoke fieldbook hero rather than a stock banner. |
| [gautamkrishnar/blog-post-workflow](https://github.com/gautamkrishnar/blog-post-workflow) | Marked README sections can update from an established RSS feed. | Add feeds only when there is a verified, regularly maintained source. |
| [antonkomarev/github-profile-views-counter](https://github.com/antonkomarev/github-profile-views-counter) | The counter measures page/proxy requests, not unique visitors. | Omit visitor counters; they do not establish the quality of the work. |

## Interaction that works on GitHub

- **Expandable stories:** GitHub supports `<details>` and `<summary>`, including Markdown content inside the disclosure. These are actual visitor-controlled interactions. [Official documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- **Theme-aware images:** `<picture>` and `prefers-color-scheme` sources select light/dark artwork, with an `<img>` fallback and descriptive alt text. [GitHub profile-writing quickstart](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)
- **Navigation:** ordinary links, linked images, and heading links provide clear paths to projects, demos, and further detail. The top row leads with *Explore Anticipy* and *Explore my portfolio*; the linked cards repeat those destinations where each story begins. [GitHub writing syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- **No embedded application:** GitHub sanitizes README HTML, including scripts and inline styles. Client-side tabs, editable terminals, and JavaScript games cannot run in the README. [GitHub rendering pipeline](https://github.com/github/markup)
- **SVG is an image here:** JavaScript is disabled in SVG image contexts, and external resources cannot normally load. Keep artwork self-contained and wrap the whole image in a link when needed. Animation is presentation, not a playable control. [MDN SVG image restrictions](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)

## Assets and updates

Keep the hero, promotion cards, and contribution artwork in the repository. This avoids a rendering-service request for every visitor and keeps a useful image available when a data refresh fails. This choice follows the reliability tradeoff documented by [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats#deploy-on-your-own-recommended).

Use one daily contribution card generated by a small Python standard-library script from public data. Label its coverage and snapshot date. Contribution counts describe recorded activity; they are not a score for skill, work quality, or overall productivity. Retain the project stories as the main evidence.

A failed refresh must preserve the last successful artifact and report failure in the workflow. It must not replace valid data with zeroes or advance the snapshot date. Commit generated changes only when they differ; provide manual dispatch for recovery.

Scheduled workflows run on the default branch and can be delayed. GitHub can disable public-repository schedules after 60 days without repository activity, so a daily schedule is not a freshness guarantee. The displayed snapshot date and last successful artifact remain useful when refreshes stop. [GitHub schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

Pin adopted Actions to verified full commit SHAs and update those pins deliberately. [GitHub versioning guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions#using-shas)

## Maintaining this profile

The README is hand-written. Original illustrations (the hero, project atlas, and Anticipy and Open Water cards) are generated from `scripts/render_artwork.py`; activity graphics and provenance come from `scripts/update_activity.py`. The artwork generator also produces the sixteen still alternatives selected for reduced motion. Both generators use Python's standard library. No personal access token or external image-rendering service is needed for activity refreshes.

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
