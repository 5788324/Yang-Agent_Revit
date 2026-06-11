# Agent Operating Model

## Purpose

This file defines how Codex, Hermes, Gemini, DeepSeek, and the user work together on YangAgent Revit.

The goal is speed with quality control.

## Codex

Codex is the project manager and technical owner.

Codex owns:

- current priorities;
- task packs for other agents;
- safety rules;
- final review;
- key implementation when a blocker is risky or unclear;
- Git commit and release decisions.

Codex should avoid spending time on bulk documentation or mechanical review when another agent can do it safely.

## Hermes / Gemini / DeepSeek

These agents are treated as auxiliary execution models.

They may do:

- read code;
- write draft documentation;
- prepare review reports;
- classify issues;
- propose low-risk patches;
- organize checklists;
- inspect external toolboxes.

They must not independently:

- change production model logic;
- approve model-changing behavior;
- claim live Revit behavior without evidence;
- merge or push;
- expand project scope.

## User

The user provides:

- real Revit context;
- sandbox run feedback;
- Gemini toolbox path;
- judgment about which tools are useful for actual work.

The user does not need to understand all implementation details.

## Review Flow

1. Codex writes a bounded task.
2. Auxiliary agent completes the task in a draft or candidate patch.
3. Codex reviews and accepts, rejects, or requests follow-up.
4. Only accepted work becomes part of the mainline.

## Live Revit Rule

No agent can replace real Revit sandbox validation.

If a behavior depends on Revit UI, Revit transactions, Undo, loaded addins, or project model state, it remains unverified until a live sandbox run confirms it.
