# Insecure Direct Object Reference

## Overview
* [Definition](#definition)
* [For Pentester](#for-pentester)
    * [Exploitation](#exploitation)
* [For Software Developer](#for-software-developer)
    * [Potential Mitigation](#potential-mitigation)
* [CVSS & CWE](#cvss-and-cwe)

---

## Definition

Insecure Direct Object Reference (IDOR) is an access control vulnerability that occurs when an application exposes a direct reference to an internal object (e.g. user ID, order number, file name, or database record) without properly verifying whether the authenticated user is authorized to access that object.

This issue typically arises when developers assume that authentication alone is sufficient to protect sensitive resources. In reality, authorization must be enforced at the object level. When this validation is missing or improperly implemented, attackers can manipulate object identifiers in requests to access data or perform actions that should be restricted to other users or higher-privileged roles.

As a result, IDOR can lead to unauthorized data disclosure, data tampering, or even complete account takeover scenarios, depending on the functionality affected.

---

## For Pentester

#### Exploitation

From a penetration testing standpoint, IDOR vulnerabilities are commonly discovered while testing authenticated features. Modern applications, especially APIs, frequently rely on client-supplied identifiers to reference backend objects. When authorization checks are weak or absent, these identifiers become a reliable attack surface.

The general approach is to authenticate as a legitimate but low-privileged user, identify requests that reference objects, and then manipulate those references to point to objects owned by other users or roles. Successful exploitation is indicated when the application returns valid data or allows unauthorized actions without enforcing access restrictions.

Typical exploitation steps include:

* Identify parameters that reference objects, including:
    * URL paths (e.g. `/api/orders/1023`)
    * Query parameters (e.g. `?user_id=45`)
    * Request bodies (e.g. `"documentId": "987"`)
* Authenticate as a valid low-privileged user (in some cases, this is not even required)
* Modify object references by:
    * Incrementing or decrementing numeric IDs
    * Reusing identifiers obtained from other responses
    * Swapping UUIDs between different accounts
* Test multiple HTTP methods:
    * `GET` → unauthorized data disclosure
    * `PUT/PATCH` → unauthorized data modification
    * `DELETE` → unauthorized object deletion
* Validate both:
    * **Horizontal privilege escalation** (accessing other users’ resources)
    * **Vertical privilege escalation** (accessing admin or restricted resources)
* Observe differences in responses:
    * HTTP status codes
    * Error messages
    * Data returned in successful responses

---

## For Software Developer

#### Potential Mitigation

Mitigating IDOR vulnerabilities requires consistently enforcing authorization at the backend for every object access. Developers should assume that any identifier sent by the client can be tampered with and must therefore be validated against the authenticated user’s permissions before any action is performed.

A robust mitigation strategy focuses on verifying object ownership or access rights at the point of use, rather than relying on implicit trust, frontend restrictions, or obscured parameters. Centralizing authorization logic also helps ensure that access control rules remain consistent as the application grows and evolves.

Effective mitigation practices include:

* Enforce **server-side authorization checks** for every request accessing an object
* Verify that the requested object **belongs to the authenticated user** or that the user has explicit permission
* Never rely on frontend checks or hidden parameters for access control
* Avoid exposing sequential or predictable identifiers when possible
* Centralize authorization logic to prevent inconsistent enforcement
* Apply **least privilege** and **deny-by-default** access control models
* Ensure authorization checks apply consistently across all API endpoints and HTTP methods
* Add automated tests and code reviews specifically targeting IDOR scenarios

---

## CVSS and CWE

IDOR vulnerabilities are commonly rated as medium to high severity, depending on the sensitivity of the affected objects and the impact of unauthorized access. Vulnerabilities that allow modification or deletion of data, or expose sensitive personal or financial information, typically receive higher scores.

* **Typical CVSS 4.0 Base Score**: **5.3 – 9.3 (Medium to High)**

* **Common CVSS 4.0 Metrics**:
    * Attack Vector (AV): Network
    * Attack Complexity (AC): Low
    * Attack Requirements (AT): None
    * Privileges Required (PR): None to Low
    * User Interaction (UI): None
    * Confidentiality Impact (VC): Low to High
    * Integrity Impact (VI): None to High
    * Availability Impact (VA): None to Low

* **Relevant CWE(s)**:
    * **CWE-639** – Authorization Bypass Through User-Controlled Key
    * **CWE-284** – Improper Access Control
    * **CWE-863** – Incorrect Authorization

> The final severity depends on the sensitivity of the exposed object and whether read-only access or write/delete actions are possible.
