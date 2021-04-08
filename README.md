
# Student thesis: Yankai Su

Working title: **IETF Network Slicing: testbed building and measurement**

## Task description

### Literature research
**Target**: Define requirements for a testbed (based on IETF drafts)
- definition of network slicing (differences/similarities between standardization organizations), non-5G vs 5G network slicing, e.g. 3GPP vs IETF vs. GSMA
- reference research (e.g. IETF) for NS, hint: see links below, _also_ lookup IETF authors on Google Scholar and study their relevant papers
- Are there recent testbeds/implementations?
- If yes, what was achieved? How is the structure/design/architecture? What should be improved (in your testbed)?
- What hardware is required for your own testbed? What kind of software? What is achievable with existing hardware/software (e.g. your PC/notebook/an existing RaspberryPI, etc.)? What not?
- **Research applications for network slicing** (e.g. tactile internet - 1ms, etc.) -> Where is a use of network slicing reasonable/meaningful? Define KPIs.

Starting point:
- https://datatracker.ietf.org/doc/draft-bestbar-spring-scalable-ns/
- https://datatracker.ietf.org/doc/draft-drake-bess-enhanced-vpn/
- https://datatracker.ietf.org/doc/draft-king-teas-applicability-actn-slicing/
- https://tools.ietf.org/html/draft-ali-spring-network-slicing-building-blocks-04#section-2
- https://tools.ietf.org/id/draft-netslices-usecases-02.html
- https://tools.ietf.org/html/draft-rokui-5g-ietf-network-slice-00
- https://sandbox.ietf.org/doc/draft-peng-teas-network-slicing/


### Testbed Design
#### A	
- Hardware: Design a reasonable/useful testbed (architecture) which provides a basement for future tests, explain your choices:
    - Why does the testbed have to look like this and not else?
- Software: Research tools (emulation vs simulation vs real implementation on hardware)
- What are the limits? Is the chosen method able to achieve the target or are there hardware limitations, etc.?
#### B
- Define the target of the test setup: performance parameters -> What should be measured (which KPIs and why?)? Which results are expected?

### Measurements
- perform measurements (extensive and detailed documentation, plots, comparisons, etc.)
- Is the testbed able to achieve the pre-defined KPIs? Is it useful for doing network slicing tests?

### Evaluation
- achieved results
- error consideration
- future work, etc.

### Outlook
- Diploma thesis: Security on SA Testbed -> investigate vulnerabilities and develop a mitigation
