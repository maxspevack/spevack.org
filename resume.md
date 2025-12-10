# Max Spevack
[max.spevack {at} gmail.com](mailto:max.spevack@gmail.com) | [LinkedIn](https://www.linkedin.com/in/maxspevack/)

## [CIQ](https://ciq.com/)
### Senior Principal Linux Architect
### Chief of Staff to the CTO
July 2025 - Present

The easiest way to describe my job is as CIQ's Linux [fixer](https://en.wikipedia.org/wiki/Fixer_(person)) and as [consigliere](https://en.wikipedia.org/wiki/Consigliere) to the CTO.

* I served as interim leader of the Automation & Delivery team for five months, during which the team:
    * Launched an automated image build pipeline with customized schedules and kickoffs.
    * Revamped secure boot signing automation and established an automated testing framework across all major cloud platforms.
    * Improved image freshness metrics from quarterly to monthly.
    * Produced customized images for [Google Distributed Cloud](https://cloud.google.com/distributed-cloud-air-gapped), AMD, and NVIDIA.
    * Drafted and helped implement a re-org creating the Release All Things (RAT) team alongside the Linux Engineering (LE) team.
    * LE is accountable for packages making it through the build system.
    * RAT is accountable for everything required to assemble those packages into repositories and images and delivering those artifacts to customers.
* Led 2026 planning for the combined LE + RAT organization.
* Hired the long-term Director for RAT and serve as coach/mentor and exception catcher for the RAT and Linux Engineering Directors.
* Established the engineering organization's weekly reporting framework, coordinated with Product on prioritization tracking, and automated the process using AI.

## [Google](http://www.google.com/)
### Senior Manager, [Google Compute Engine](https://cloud.google.com/compute/)
Jul 2021 - Jul 2023

I formed and led the ~50 person GCE Fleet organization, owning the development, qualification, and release velocity of the kernel + hypervisor bundle running on all GCE hosts. The team owned the lifecycle and versioning of GCE host pools.

* Assembly, qualification, deployment, and operation of the standard GCE fleet, with a primary focus on velocity and heterogeneity metrics to inform our engineering priorities. One innovation was the amusingly named “mandatory experiments” policy to reduce rollbacks.
* Development, initial deployment, and operation of a “stable fleet” for enterprise customers with greater sensitivities to change windows. This functionality included automated notifications, migration window (with live and managed migrations), and specific rate-of-change guarantees. Later, this stable fleet concept expanded to fine-grained GCE host pools.
* White-gloves engineering treatment for ultra-VIP GCE customers.

## [Amazon Web Services](http://aws.amazon.com/)
### General Manager, [Amazon Linux](https://aws.amazon.com/linux/amazon-linux-2023/)
Jul 2019 - Jun 2021
### Senior Manager, [Open Source](https://aws.amazon.com/opensource/)
Jul 2019 - Jun 2021

I led the >100 person organization that owned Amazon Linux – available as a [public EC2 image](https://aws.amazon.com/amazon-linux-ami/) and as an internal server OS for both [AWS](http://aws.amazon.com/) and Amazon's [retail business](http://www.amazon.com/) – as well as Amazon’s [Open Source Program Office](https://en.wikipedia.org/wiki/Open_Source_Program_Office) (OSPO).

I was ultimately accountable for Amazon’s Linux portfolio – product and engineering, including:

* Creation of the [Amazon Linux 1](https://aws.amazon.com/amazon-linux-ami/) (AL1) [extended support plan](https://aws.amazon.com/blogs/aws/update-on-amazon-linux-ami-end-of-life/) based on many customer requests.
* Continued development of [Amazon Linux 2](https://aws.amazon.com/amazon-linux-ami/) (AL2), including the addition of [kernel live patching](https://docs.aws.amazon.com/linux/al2/ug/al2-live-patching.html).
* Delivered the fully-approved PR/FAQ for [Amazon Linux 2023](https://aws.amazon.com/linux/amazon-linux-2023/).
* Launched GA of [Bottlerocket](https://bottlerocket.dev/), a Linux-based OS purpose-built for hosting containers on multiple platforms (AWS, Bare Metal, VMWare) as well as orchestrators (EKS, ECS).
* Prioritized internal migration to AL2 by delivering in-place upgrades from AL1.
* Rebuilt the CVE ingestion infrastructure, improving Amazon Linux security tracking and [publication](https://alas.aws.amazon.com/).

With the OSPO, I re-organized the team to take a tooling-based approach to its charter, with a specifically increasing the number of cases (including GitHub administration and M&A work) that could be resolved either automatically or by customers directly and creating tooling to reduce the team’s manual labor.

* Launched “Open Source Champions”, a program to deputize Principal Engineers in organizations to make open-source related decisions directly, pushing ownership to the customer.
* Delivered and received approval from AWS leadership on “Open Source Decision Making Guidelines”, a mechanism for teams to determine if and when to open source their code.
* Developed and operationalized an “Open Source Readiness Review”, ensuring that teams making the decision to open source their code had done so in a way that would result in successful community projects, bolstering Amazon’s open source reputation.

## [Google](http://www.google.com/)
### Senior Manager, [Google Compute Engine](https://cloud.google.com/compute/)
Feb 2016 - Jun 2019

I led the three GCE engineering teams accountable for:
* KVM, both in Google's kernel and the relationship with the upstream community.
* Building, qualifying, and measuring GCE host kernel quality and deployment velocity.
* New product introduction and end-to-end customer experience for CPUs, GPUs, memory-optimized instances, and nested virtualization.
* Live migration functionality and efficiency.

Customer-facing launches include [Skylake](https://cloud.google.com/blog/products/gcp/compute-engine-updates-bring-skylake-ga-extended-memory-and-more-vm-flexibility) and [Cascade Lake](https://cloud.google.com/blog/products/compute/introducing-compute-and-memory-optimized-vms-for-google-compute-engine) CPUs, SAP-certified large memory instances ([ultramem](https://cloud.google.com/blog/products/gcp/now-shipping-ultramem-machine-types-with-up-to-4tb-of-ram), [m2](https://cloud.google.com/blog/products/compute/introducing-compute-and-memory-optimized-vms-for-google-compute-engine)), Nvidia GPUs ([V100](https://cloud.google.com/blog/products/compute/tesla-v100-gpus-are-now-generally-available), [P4 with GRID support](https://cloud.google.com/blog/products/gcp/introducing-nvidia-tesla-p4-gpus-accelerating-virtual-workstations-and-ml-inference-compute-engine), [T4](https://cloud.google.com/blog/products/compute/efficiently-scale-ml-and-other-compute-workloads-on-nvidias-t4-gpu-now-generally-available)), and [nested virtualization](https://cloud.google.com/blog/products/gcp/introducing-nested-virtualization-for). The team received four of Google's "Cloud Feat of Engineering" awards for response to [Spectre / Meltdown](https://blog.google/products/google-cloud/answering-your-questions-about-meltdown-and-spectre/), response to [L1TF](https://cloud.google.com/blog/products/gcp/protecting-against-the-new-l1tf-speculative-vulnerabilities), nested virtualization, and the SAP-certified large-memory instances.

## [Amazon Web Services](http://aws.amazon.com/)
### Manager, Linux Kernel & Operating Systems
Aug 2011 - Jan 2016

I led the team accountable for Amazon Linux. The team's primary objective was to build, qualify, deploy, and support multiple versions of Amazon Linux. This included [feature](https://aws.amazon.com/amazon-linux-ami/2015.09-release-notes/) [development](https://aws.amazon.com/amazon-linux-ami/2015.03-release-notes/) and integration with EC2, building kernel and userspace packages, [security updates](https://alas.aws.amazon.com/), and deploying packages and images. The team owned the infrastructure and tooling to build packages, compose images, stage repositories, perform automated testing, and gather metrics.

I spent a year simultaneously managing two distinct teams – the Amazon Linux team discussed above, and the team responsible for qualifications of new [EC2 instance types](https://aws.amazon.com/ec2/instance-types/) and platforms. During that time, the qualifications team developed tooling, test coverage, and reporting for the [T2](https://aws.amazon.com/blogs/aws/low-cost-burstable-ec2-instances/), [C4](https://aws.amazon.com/blogs/aws/now-available-new-c4-instances/), and [D2](https://aws.amazon.com/blogs/aws/next-generation-of-dense-storage-instances-for-ec2/) launches. I assisted with the hiring of a manager to transition the qualifications team over to, and I helped with onboarding, training, and a smooth handoff of responsibilities. I also spent 18 months as part of the EC2 Operations team. I was responsible for a weekly summary of all EC2 operational issues including discussion of customer impacting events, status of key metrics, and overall EC2 fleet health.

## [Red Hat](http://www.redhat.com/)
### Manager, Open Source Community Architecture
Feb 2008 - Aug 2011
### [Fedora Project Leader](https://docs.fedoraproject.org/en-US/council/fpl/)
Feb 2006 - Feb 2008
### Linux Systems Engineer
Aug 2004 - Feb 2006

I was ultimately accountable for the [Fedora Project](https://getfedora.org/), a collaboration between Red Hat and a worldwide community of free software contributors whose flagship project is the [Fedora Linux distribution](http://en.wikipedia.org/wiki/Fedora_(operating_system)). I was responsible for Red Hat employees and community contributors in numerous areas: product and engineering, operations, marketing, branding, community, communications, public speaking ([LWN](http://lwn.net/Articles/237700/), [Slashdot](https://slashdot.org/story/06/08/17/177220/fedora-project-leader-max-spevack-responds), [Ohio Linux Fest](http://www.youtube.com/watch?v=JC6URXglbO4)), legal, financial, budgeting, and hiring.

After two years I split the role into several parts – a continued Fedora Project Leader, a new Fedora Engineering Manager, and a new Open Source Community Architecture team, which I led. This was a global team, with a charter to deliver highly leveraged growth, development, and success of communities strategic to Red Hat's business and brand, including:

* Ensuring that the free software community was an equal partner in the creation of Red Hat's products, and that the [Open Source Way](http://www.theopensourceway.org/) was institutionalized in Red Hat’s culture.
* Stewardship and senior-level leadership of the Fedora Project.
* Merging the Open Source Way and education, founding the [Teaching Open Source](http://teachingopensource.org/) community.

## [Verisign](http://en.wikipedia.org/wiki/Verisign)
### Quality Assurance Engineer
Oct 2002 - Aug 2004

## Education
### BS [Computer Science](http://cs.stanford.edu/), [Stanford University](http://www.stanford.edu/)
Sep 1998 - Jun 2002
