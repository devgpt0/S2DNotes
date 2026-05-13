# Project 05: Helpdesk Ticket SLA Tracker

## Estimated Time
4 to 6 hours

## Goal
Build a ticket tracking backend module with SLA monitoring.

## Functional Requirements
- Create ticket with priority and created time.
- Assign ticket to support agent.
- Update status (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`).
- Compute SLA due time by priority.
- List breached tickets.

## Non-Functional Requirements
- Status updates must be logged.
- Closed tickets cannot be updated.

## Concepts Practiced
- `Map<String, TicketRecord>` tickets
- `List<String>` audit logs
- filtering based on time/status

## HLD
- `TicketService`
- `SlaService`
- `AssignmentService`
- `ReportService`

## LLD
- `createTicket(ticketMap, ticket): String`
- `assignTicket(ticketMap, ticketId, agentId): boolean`
- `updateStatus(ticketMap, ticketId, status): boolean`
- `computeDueTime(priority, createdAt): LocalDateTime`
- `findBreachedTickets(ticketMap, now): List<TicketRecord>`

## Passing Criteria
- SLA due times generated correctly.
- Breach list matches priority rules.
- Closed ticket update is blocked.

## Implementation Roadmap
1. Build ticket model.
2. Add CRUD/state updates.
3. Add SLA logic.
4. Add breach report.
