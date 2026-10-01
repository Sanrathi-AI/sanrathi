# Sanrathi changes to Presenton

Apache License 2.0, section 4(b), requires that any file we modify "carry
prominent notices stating that [we] changed the files". This document is
that notice at the repository level; every changed text file also carries a
one-line `Modified by Sanrathi, 2026` comment at the top (added by
`sanrathi/mark_changed_files.py`).

Fork point: `presenton/presenton` commit `2dcbde77` (main, checked 2026-09-30).
All Sanrathi work lives on the `sanrathi` branch; `main` stays a clean mirror
of upstream (see section 10 of the build guide, "Staying up to date").

## What changed, by purpose

1. **Ops** (`docker-compose.yml`): the `production` service is bound to
   `127.0.0.1` only, the `1455` OAuth callback port is dropped, and
   `host.docker.internal` is mapped explicitly for Linux Docker.
2. **Brand**: Presenton's name, logos, favicon, splash screen and purple UI
   accent were replaced with Sanrathi's (placeholder meerkat mark until the
   real artwork is ready). Presenton's Discord/GitHub-star buttons and
   external links were removed or repointed to sanrathi.com. See
   `sanrathi/find_brand_text.py` and `sanrathi/recolor_ui.py`.
3. **Templates**: two new templates, `templates/sanrathi-paper` and
   `templates/sanrathi-ink`, cloned from the built-in `general` template with
   colours swapped to Sanrathi's ink/paper/radium palette (including the
   decorative PNGs in each template's `static/` folder, not just
   `template.json`). They are shown first in both the API's template order
   (`servers/fastapi/constants/presentation.py`) and the create-presentation
   picker's client-side order (`useTemplateSummaries.ts`).
4. **Compliance**: a new `/licenses` page shows the Presenton attribution,
   the AI model's license, font licenses, and links to the full `LICENSE`
   and `NOTICE` text (new API route `app/api/licenses/[file]/route.ts`).
5. **Bug fixes found while testing the fork end-to-end** (not Sanrathi
   features — genuine issues in how this version behaves with
   `CAN_CHANGE_KEYS=false`, the setting the guide uses to lock the Slide
   Maker down):
   - `start.js` only synced `.env`'s `LLM`/`OLLAMA_*` settings into
     `app_data/userConfig.json` when `CAN_CHANGE_KEYS=true`. With it `false`,
     `/api/runtime-config` always reported the provider as unconfigured and
     the UI looped between `/` and `/upload` after login.
   - `/api/runtime-config` sent `AUTH_PASSWORD_HASH` and `AUTH_SECRET_KEY`
     (the JWT signing key) to every logged-in user; the redaction pattern in
     `lib/runtime-provider-config.ts` only matched `*_API_KEY`/`PASSWORD`/
     token-shaped field names.
   - `migrate_provider_settings_from_file` (`services/provider_settings.py`)
     only imported `userConfig.json` into the database on the *first* boot.
     On every later boot it mirrored the database back onto the file instead,
     so a `.env` change (for example turning on Pixabay images) silently
     reverted after a restart, because the stale database row kept winning
     over the freshly `.env`-derived file.
6. **Gateway** (`gateway/`, new, not part of Presenton): the Sanrathi
   backend's watermark stamper and the `/v1/slides/*` router that turns a
   topic or a lecture transcript into a Slide Maker job.
7. **Tooling** (`sanrathi/`, new, not part of Presenton): the scripts used to
   make and verify the above (brand finder, recolour, template maker,
   placeholder logo generator, this change-marking script, and the Linux
   Ollama/firewall setup script).

## Modified files (existing Presenton files)

Each carries a `Modified by Sanrathi, 2026` comment, except the binary image
files listed at the end, which cannot carry a text comment.

```
docker-compose.yml
servers/fastapi/constants/presentation.py
servers/nextjs/app/api/licenses/[file]/route.ts
servers/nextjs/app/ConfigurationInitializer.tsx
servers/nextjs/app/globals.css
servers/nextjs/app/icon1.svg
servers/nextjs/app/layout.tsx
servers/nextjs/app/not-found.tsx
servers/nextjs/app/(presentation-generator)/components/ImageEditorToolbar.tsx
servers/nextjs/app/(presentation-generator)/components/TemplateListUi.tsx
servers/nextjs/app/(presentation-generator)/components/V1ContentRender.tsx
servers/nextjs/app/(presentation-generator)/components/V1SelectEdit.tsx
servers/nextjs/app/(presentation-generator)/custom-template/CustomTemplatePage.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/admin/AdminPanel.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/admin/page.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/community/components/CommunityDesignPreviewDialog.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/community/components/CommunityPage.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/Components/DashboardNav.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/Components/DashboardSidebar.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/dashboard/components/DashboardPage.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/dashboard/components/EmptyState.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/dashboard/components/LegacyPresentationsTable.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/dashboard/components/PresentationCard.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/licenses/page.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/ImageProvider.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/page.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/PrivacySettings.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/SettingPage.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/SettingSideBar.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/UserAccountSettings.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/settings/WebSearchProvider.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/templates/components/CreateCustomTemplate.tsx
servers/nextjs/app/(presentation-generator)/(dashboard)/templates/components/TemplatePanel.tsx
servers/nextjs/app/(presentation-generator)/documents-preview/components/DocumentPreviewPage.tsx
servers/nextjs/app/(presentation-generator)/hooks/useTemplateSummaries.ts
servers/nextjs/app/(presentation-generator)/outline/components/CustomTemplateCard.tsx
servers/nextjs/app/(presentation-generator)/outline/components/GenerateButton.tsx
servers/nextjs/app/(presentation-generator)/outline/components/OutlineContent.tsx
servers/nextjs/app/(presentation-generator)/outline/components/OutlineItem.tsx
servers/nextjs/app/(presentation-generator)/outline/components/OutlinePage.tsx
servers/nextjs/app/(presentation-generator)/outline/components/OutlinePromptBar.tsx
servers/nextjs/app/(presentation-generator)/outline/components/OutlineStandardHeader.tsx
servers/nextjs/app/(presentation-generator)/outline/components/TemplateSelection.tsx
servers/nextjs/app/(presentation-generator)/outline/page.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/chat/chat-prompts.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/chat/chat-widgets.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/Chat.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/KeyboardShortcutsDialog.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/NewSlide.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/PresentationActions.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/PresentationHeader.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/PresentationMode.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/PresentationPage.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/SidePanel.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/SlideActionBar.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/SlideContent.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/SlideThumbnailCard.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/SortableListItem.tsx
servers/nextjs/app/(presentation-generator)/presentation/components/StreamingGenerationMetrics.tsx
servers/nextjs/app/(presentation-generator)/presentation/hooks/usePresentationData.ts
servers/nextjs/app/(presentation-generator)/_shared/TemplateV2PromptOverlay.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/EditorActionBar.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/LayoutsPanel.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/ResponsiveSlideFrame.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/TemplateEditorHeader.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/TemplatePreviewSidePanels.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/TemplatePreviewStates.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/editor/ThumbnailStrip.tsx
servers/nextjs/app/(presentation-generator)/template-preview/components/TemplatePreviewClient.tsx
servers/nextjs/app/(presentation-generator)/upload/components/AdvanceSettings.tsx
servers/nextjs/app/(presentation-generator)/upload/components/CommunityPresentationFilters.tsx
servers/nextjs/app/(presentation-generator)/upload/components/CommunityReferencePicker.tsx
servers/nextjs/app/(presentation-generator)/upload/components/ConfigurationSelects.tsx
servers/nextjs/app/(presentation-generator)/upload/components/CurrentConfig.tsx
servers/nextjs/app/(presentation-generator)/upload/components/GenerationModeDialog.tsx
servers/nextjs/app/(presentation-generator)/upload/components/LanguageSelector.tsx
servers/nextjs/app/(presentation-generator)/upload/components/PromptInput.tsx
servers/nextjs/app/(presentation-generator)/upload/components/SupportingDoc.tsx
servers/nextjs/app/(presentation-generator)/upload/page.tsx
servers/nextjs/components/AdvancedTextProviderSettings.tsx
servers/nextjs/components/Auth/AuthGate.tsx
servers/nextjs/components/LLMSelection.tsx
servers/nextjs/components/OllamaConfig.tsx
servers/nextjs/components/OnBoarding/FinalStep.tsx
servers/nextjs/components/OnBoarding/OnboardingPresentonAccount.tsx
servers/nextjs/components/OnBoarding/OnBoardingSlidebar.tsx
servers/nextjs/components/OnBoarding/PresentonMode.tsx
servers/nextjs/components/slide-editor/images/IconsEditor.tsx
servers/nextjs/components/slide-editor/images/ImageToolbar.tsx
servers/nextjs/components/slide-editor/infographics/InfographicEditorContent.tsx
servers/nextjs/components/slide-editor/infographics/InfographicPlainTextEditor.tsx
servers/nextjs/components/slide-editor/layout/ContainerToolbarControls.tsx
servers/nextjs/components/slide-editor/layout/InfographicToolbarControls.tsx
servers/nextjs/components/slide-editor/layout/LayoutToolbar.tsx
servers/nextjs/components/slide-editor/selection/MultiSelectionToolbar.tsx
servers/nextjs/components/slide-editor/selection/SelectionTransformers.tsx
servers/nextjs/components/slide-editor/shapes/ShapeToolbar.tsx
servers/nextjs/components/slide-editor/surface/nodes.tsx
servers/nextjs/components/slide-editor/surface/TemplateV2KonvaSlide.tsx
servers/nextjs/components/slide-editor/tables/TableInlineEditor.tsx
servers/nextjs/components/slide-editor/tables/TemplateV2TableElement.tsx
servers/nextjs/components/slide-editor/text/TemplateV2InlineEditor.tsx
servers/nextjs/components/slide-editor/text/TextToolbar.tsx
servers/nextjs/components/slide-editor/text/TiptapInlineTextEditor.tsx
servers/nextjs/components/slide-editor/toolbar/inlineStyles.ts
servers/nextjs/components/ui/overlay-loader.tsx
servers/nextjs/components/ui/presenton-splash-loader.tsx
servers/nextjs/components/ui/progress-bar.tsx
servers/nextjs/components/ui/switch.tsx
servers/nextjs/lib/runtime-provider-config.ts
servers/fastapi/services/provider_settings.py
start.js
```

Binary files modified (placeholder art; recoloured or replaced, no comment
possible):

```
servers/nextjs/app/apple-icon.png
servers/nextjs/app/favicon.ico
servers/nextjs/app/icon2.png
servers/nextjs/public/Logo.png
servers/nextjs/public/logo-white.png
servers/nextjs/public/logo-with-bg.png
servers/nextjs/public/Presenton_Splash.png
templates/sanrathi-paper/static/*.png
templates/sanrathi-ink/static/*.png
```

## New files (not part of Presenton)

```
gateway/                          Sanrathi backend <-> Slide Maker bridge
sanrathi/                         helper scripts referenced above
templates/sanrathi-paper/         new template, cloned from templates/general
templates/sanrathi-ink/           new template, cloned from templates/general
servers/nextjs/app/api/licenses/[file]/route.ts
servers/nextjs/app/(presentation-generator)/(dashboard)/licenses/page.tsx
SANRATHI_CHANGES.md               this file
```

## Regenerating this list

```
git diff --name-status <fork-point>..HEAD -- servers templates start.js docker-compose.yml
python sanrathi/mark_changed_files.py <fork-point>
```
