<p align="center">
  <a href="https://byo.dev">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/byo-oss/.github/main/profile/assets/banner-dark.png">
      <img alt="BYO: the SaaS you'd rent, as plugins you own." src="https://raw.githubusercontent.com/byo-oss/.github/main/profile/assets/banner-light.png" width="100%">
    </picture>
  </a>
</p>

**BYO** is a set of open-source packages for [better-auth](https://better-auth.com) apps. Notifications, support and plan limits, the things you'd otherwise rent as SaaS, run inside your app as libraries. They keep their data in your database and know your users and organizations.

[**byo.dev**](https://byo.dev) · [Docs](https://byo.dev/docs) · [Conventions](https://github.com/byo-oss/conventions/blob/main/SPEC.md) · [npm](https://www.npmjs.com/org/byo-oss)

## Packages

| Package | What it gives you | When you outgrow it | |
|---|---|---|---|
| [`@byo-oss/notifications`](https://github.com/byo-oss/notifications) | A bell, an inbox and email follow-up for anything that went unread | Knock · Novu · Courier | ![npm](https://img.shields.io/npm/v/@byo-oss/notifications?label=npm&color=111111) [Docs](https://byo.dev/docs/notifications/quickstart) |
| [`@byo-oss/support`](https://github.com/byo-oss/support) | Tickets, contacts and agent replies inside your app, with email in and out | Zendesk · Plain · Front | ![npm](https://img.shields.io/npm/v/@byo-oss/support?label=npm&color=111111) [Docs](https://byo.dev/docs/support/quickstart) |
| [`@byo-oss/entitlements`](https://github.com/byo-oss/entitlements) | Plans, features, limits and usage from one typed catalog. Stripe says which plan an org bought; this decides what it allows | Autumn · Stigg · Schematic | ![npm](https://img.shields.io/npm/v/@byo-oss/entitlements?label=npm&color=111111) [Docs](https://byo.dev/docs/entitlements/quickstart) |
| [`@byo-oss/mailer`](https://github.com/byo-oss/mailer) | The email sender the packages share: Wraps, SES or email-sdk | your provider's SDK | ![npm](https://img.shields.io/npm/v/@byo-oss/mailer?label=npm&color=111111) [Docs](https://byo.dev/docs/mailer/introduction) |
| [`@byo-oss/core`](https://github.com/byo-oss/core) | One event bus, one cron route and one org-cleanup call for every BYO plugin | | ![npm](https://img.shields.io/npm/v/@byo-oss/core?label=npm&color=111111) |

Also here: [`conventions`](https://github.com/byo-oss/conventions), the rules that make the packages one system, and [`site`](https://github.com/byo-oss/site), the source of byo.dev.

## How they fit together

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/byo-oss/.github/main/profile/assets/how-it-fits-dark.png">
    <img alt="Diagram. Your app runs better-auth, which loads the BYO plugins (notifications, support, entitlements). @byo-oss/core reads that plugin list to give them one event bus, one cron sweep and one cleanup call. Providers sit outside: Wraps, the mailer and Stripe. The conventions underneath keep them one system." src="https://raw.githubusercontent.com/byo-oss/.github/main/profile/assets/how-it-fits-light.png" width="100%">
  </picture>
</p>

- **One identity.** Every package is addressed to your better-auth users and organizations. Delete a user or an org and their rows go with them. `@byo-oss/core` clears an org's or a member's data across every installed package in one call.
- **One event stream.** Packages emit events after the write commits (`support.ticket.created`, `notifications.delivery.failed`, ...). You pass the same `onEvent` to each plugin and decide where events go: an in-app notification, an activity log, a webhook.
- **One cron route.** Delayed email, retries, auto-closing and pruning are background work a plugin can't run itself. `sweepAll(auth)` runs every installed package's work from a single route.
- **One way out.** Each product ships a JSON data export, a documented schema, a clean uninstall and a mapping to the tool you'd move to.

## Using them

**1. Start with the one you need.** Install it, add it to `plugins`, migrate, drop in the component. Each quickstart is a handful of steps.

| If you need to... | Install |
|---|---|
| tell users something happened in your app | `@byo-oss/notifications` |
| let customers ask for help, and give staff a queue | `@byo-oss/support` |
| stop scattering plan names and limits across your API, web app and pricing page | `@byo-oss/entitlements` |
| send email from your own plugin code | `@byo-oss/mailer` |
| run two or more of the above | add `@byo-oss/core` |

**2. Add the next one.** The packages share the better-auth database, so a second one is another line in `plugins`. `organization()` goes first because the others' tables reference it.

```ts
// lib/auth.ts
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins/organization";
import { createEventBus } from "@byo-oss/core";
import { inbox } from "@byo-oss/notifications";
import { support } from "@byo-oss/support";
import { entitlements } from "@byo-oss/entitlements";
import { catalog } from "./catalog";

const staffOrganizationId = process.env.STAFF_ORGANIZATION_ID;

// One handler for every package's events. Send them wherever you like.
const onEvent = createEventBus([
  async (event) => {
    if (event.type === "support.agent.replied" && event.userId) {
      await auth.api.notify({ body: { userId: event.userId, type: event.type, title: "New reply to your ticket" } });
    }
  },
]);

export const auth = betterAuth({
  // ...your existing config
  plugins: [
    organization(), // before the others
    inbox({ onEvent }),
    support({ staffOrganizationId, onEvent }),
    entitlements({ catalog, staffOrganizationId, onEvent }),
  ],
});
```

```ts
// app/api/cron/byo/route.ts: run it every minute from any scheduler
import { sweepAll } from "@byo-oss/core";
import { auth } from "@/lib/auth";

export async function GET() {
  return Response.json(await sweepAll(auth, { budgetMs: 20_000 }));
}
```

Each package's quickstart covers what this sketch leaves out: access-control statements, the client plugin and the React components.

**3. Leave when you outgrow one.** Run the new tool beside the package, backfill from the JSON export, switch the call sites, then uninstall and drop the tables in the documented order. Each product documents the field mapping to its exit targets.

## With a coding agent

Notifications, support and entitlements each ship an agent skill that walks through setup, plus an `AGENTS.md` and `llms.txt`:

```sh
npx skills add byo-oss/notifications
npx skills add byo-oss/support
npx skills add byo-oss/entitlements
```

## Ground rules

- **Libraries, not services.** No dashboards to sign up for and nothing to deploy. A package runs in your app and stores its data in your database.
- **One system.** The [conventions](https://github.com/byo-oss/conventions/blob/main/SPEC.md) are what let packages share identity, permissions, events and background work. A new package is built to them from day one.
- **MIT licensed.** Community project, not affiliated with the better-auth team.

Found a bug or want a package we don't have? Open an issue on the repo it belongs to, or on [conventions](https://github.com/byo-oss/conventions/issues) if it is about how packages work together.
