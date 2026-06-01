import sqlite3
import os

def init_database():
    # Agar purani incomplete database file hai toh use delete karke fresh banayenge
    if os.path.exists("tatasteel_ld.db"):
        os.remove("tatasteel_ld.db")
        
    conn = sqlite3.connect("tatasteel_ld.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fixed_faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)

    # SARA DATA: All 25 Roles from your CSV with 5 Fixed QA each
    all_roles_data = [
        # 1. Crane Operator
        ("Crane Operator", "What is the standard hand signal for emergency stop?", "Extend both arms horizontally and move them rapidly back and forth."),
        ("Crane Operator", "What are the daily pre-operational checks for overhead cranes?", "Check hoist limit switches, wire rope condition for frays, and brake functionality."),
        ("Crane Operator", "What is the maximum wind speed allowable for safe crane operations?", "Suspend all operations if continuous wind speeds exceed 45 km/h."),
        ("Crane Operator", "What safety clearance must a crane maintain from power lines?", "Always maintain a minimum safe distance of 5 meters from active overhead power lines."),
        ("Crane Operator", "How often should load testing be conducted on cranes?", "Statutory load testing must be performed once every 12 months by a certified entity."),

        # 2. Blast Furnace Technician
        ("Blast Furnace Technician", "What is the primary hazard during tuyere changing?", "High-pressure hot gas blowout, thermal radiation burns, and exposure to toxic Carbon Monoxide (CO)."),
        ("Blast Furnace Technician", "What PPE is mandatory during liquid metal tapping?", "Aluminized fire-retardant suit, full face shield, heavy-duty leather gloves, and safety shoes."),
        ("Blast Furnace Technician", "What is the safety limit for Carbon Monoxide (CO) in the workspace?", "The permissible exposure limit is 30 ppm for an 8-hour shift. Evacuate immediately if it crosses 50 ppm."),
        ("Blast Furnace Technician", "What to do in case of a cooling plate failure?", "Immediately report to the control room, isolate the water line safely, and switch to emergency cooling."),
        ("Blast Furnace Technician", "What is the correct response to a blast furnace hanging issue?", "Initiate a controlled 'slip' or reduce blast volume/temperature as per SOP guidelines."),

        # 3. Electrician
        ("Electrician", "What is the primary rule of LOTO (Lockout/Tagout)?", "Never work on an electrical circuit without isolating the source, locking the breaker, and putting your personal safety tag."),
        ("Electrician", "What is the safe distance to maintain to prevent Arc Flash injuries?", "Maintain a minimum boundary distance of 4 feet (1.2 meters) for low voltage systems."),
        ("Electrician", "What class of fire extinguisher is used for electrical fires?", "Always use a Class C or Carbon Dioxide (CO2) extinguisher. Never use water."),
        ("Electrician", "What is the maximum allowed leakage current for portable tools?", "Portable electrical tools must not exceed a leakage current threshold of 0.5 mA."),
        ("Electrician", "How do you verify if a line is dead after isolation?", "Use a certified and calibrated multi-meter to test phase-to-phase and phase-to-earth lines."),

        # 4. Safety Officer
        ("Safety Officer", "What is the primary objective of the Zero Harm policy?", "To achieve zero fatalities, zero injuries, and zero occupational health issues across all plant locations."),
        ("Safety Officer", "How is a Near-Miss incident defined and reported?", "A Near-Miss is an unplanned event that did not result in injury or damage but had the potential to do so. It must be logged within 24 hours on the safety portal."),
        ("Safety Officer", "What are the core components of a Job Safety Analysis (JSA)?", "Break down the job into steps, identify hazards for each step, and define control measures for each hazard."),
        ("Safety Officer", "What is the frequency of mandatory safety audits in high-risk zones?", "High-risk operational zones must undergo comprehensive safety audits at least once every month."),
        ("Safety Officer", "What are the key responsibilities during an onsite emergency evacuation?", "Guide workforce to the nearest assembly point, conduct headcounts, and coordinate with the emergency response team."),

        # 5. Mechanical Technician
        ("Mechanical Technician", "What is the rule for lubrication during machine operation?", "Never lubricate or clean a machine manually while it is in motion unless an automated remote system is installed."),
        ("Mechanical Technician", "How do you prevent shaft misalignment during pump installation?", "Use dial indicators or laser alignment tools to ensure alignment matches the manufacturer specification within 0.05mm."),
        ("Mechanical Technician", "What safety measure is required before repairing a conveyor belt?", "Isolate the drive motor, apply LOTO, and securely clamp the belt to prevent tension snaps."),
        ("Mechanical Technician", "What is the correct way to check torque on structural bolts?", "Always use a calibrated torque wrench to tighten bolts in a cross-pattern sequence to the specified torque limit."),
        ("Mechanical Technician", "What indicates a failing bearing during inspection?", "Abnormal high temperature (above 80 degrees C), unusual vibration, or metallic grinding noise."),

        # 6. Welding Technician
        ("Welding Technician", "What shade of filter lens is required for arc welding?", "A minimum of Shade 10 to 12 filter lens is mandatory to protect eyes from harmful UV and infrared rays."),
        ("Welding Technician", "Why is a hot work permit required before welding?", "To ensure the area is free of flammable gases/materials, fire extinguishers are on standby, and safety checks are complete."),
        ("Welding Technician", "What is the danger of welding on galvanized steel?", "It releases highly toxic Zinc Oxide fumes, which can cause metal fume fever. Proper ventilation and respirators are mandatory."),
        ("Welding Technician", "How should oxygen and acetylene cylinders be stored?", "Stored upright, secured with chains, and separated by a minimum distance of 20 feet or a fire-resistant wall."),
        ("Welding Technician", "What is the rule for grounding a welding machine?", "The workpiece and the frame of the welding machine must be grounded to a permanent electrical earth line."),

        # 7. Production Supervisor
        ("Production Supervisor", "What are the 5S principles used in lean manufacturing?", "Sort (Seiri), Set in order (Seiton), Shine (Seiso), Standardize (Seiketsu), and Sustain (Shitsuke)."),
        ("Production Supervisor", "How do you handle a production bottleneck on the line?", "Analyze the cycle time of each workstation, reallocate manpower, or balance the workload to match the Takt time."),
        ("Production Supervisor", "What is OEE and how is it calculated?", "Overall Equipment Effectiveness. It is calculated by multiplying Availability x Performance x Quality."),
        ("Production Supervisor", "What step should be taken if product quality falls below tolerance?", "Immediately halt the affected process section, trigger a root cause analysis, and isolate the non-conforming batch."),
        ("Production Supervisor", "How often should shift handover meetings be conducted?", "At the exact end of every shift, lasting no more than 15 minutes to clear logbooks and ongoing issues."),

        # 8. Mining Engineer
        ("Mining Engineer", "What is the main hazard of slope failure in open-cast mines?", "Massive rockfall or landslide that can bury heavy machinery and workers. Continuous slope monitoring radar is required."),
        ("Mining Engineer", "How is dust managed in mining hauling roads?", "By continuous pressurized water spraying systems and using environment-friendly dust-suppressant chemicals."),
        ("Mining Engineer", "What precaution is taken before blasting operations?", "Evacuate the danger zone (minimum 500m radius), sound the siren warning, and secure all entry pathways."),
        ("Mining Engineer", "What is the purpose of roof bolting in underground mines?", "To bind loose rock strata together into a solid beam, preventing roof collapses and cave-ins."),
        ("Mining Engineer", "How often must mine ventilation air quality be tested?", "Tested continuously via automated gas monitors, with manual cross-checks performed at least once per shift."),

        # 9. Quality Inspector
        ("Quality Inspector", "What is a non-conformance report (NCR)?", "A formal document issued when a raw material or finished steel product fails to meet the specified ASTM/IS quality standards."),
        ("Quality Inspector", "How is the hardness of a steel coil tested?", "Using Rockwell or Brinell hardness testing machines on a cut sample from the edge of the coil."),
        ("Quality Inspector", "What do ultrasonic tests detect in steel slabs?", "Internal defects like blowholes, cracks, inclusions, or laminations without destroying the material."),
        ("Quality Inspector", "What is the procedure if a gauge variation is detected?", "Mark the defective coil section, inform the rolling mill operators to recalibrate, and update the hold status."),
        ("Quality Inspector", "How often should inspection instruments be calibrated?", "All master gauges and micrometers must be calibrated every 6 months against national standards."),

        # 10. Automation Engineer
        ("Automation Engineer", "What protocol is commonly used for PLC-to-SCADA communication?", "Modbus TCP/IP, Profinet, or OPC UA protocols are standard for real-time industrial data transfer."),
        ("Automation Engineer", "What is the first step when a PLC goes into 'Fault' mode?", "Connect the programming laptop, read the processor diagnostic buffer log, and check for I/O module failures."),
        ("Automation Engineer", "Why are optical isolators used in industrial control loops?", "To protect sensitive PLC CPU circuits from high voltage surges or electrical noise coming from the field fields."),
        ("Automation Engineer", "What does a 4-20mA current loop signal indicate?", "It is an analog signal standard where 4mA represents the minimum scale (0%) and 20mA represents the maximum scale (100%)."),
        ("Automation Engineer", "What safety measure is mandatory before deploying a new PLC code?", "Run a full simulation test on a test bench before uploading code to active factory machinery."),

        # 11. Warehouse Manager
        ("Warehouse Manager", "What is the maximum stacking height for finished steel sheets?", "Steel sheet bundles should not be stacked more than 3 tiers high to prevent collapse and floor damage."),
        ("Warehouse Manager", "What is the FIFO method in inventory management?", "First-In, First-Out. It ensures older inventory is dispatched first to prevent material degradation or rusting."),
        ("Warehouse Manager", "What safety hazard is unique to steel coil storage yards?", "Coils rolling due to improper chocking. Heavy-duty wooden or polyurethane wedges must always secure both sides."),
        ("Warehouse Manager", "How should hazardous chemicals in the store be segregated?", "Stored in a dedicated ventilated room with containment bunds, organized by their chemical compatibility charts."),
        ("Warehouse Manager", "What is the protocol for handling a damaged storage rack?", "Unload all materials from the affected bay immediately, tape off the area, and issue an urgent engineering repair notice."),

        # 12. Shift Incharge
        ("Shift Incharge", "What is the primary duty of a Shift Incharge during a critical accident?", "Stop operations in the affected zone, trigger the emergency siren, initiate first aid/evacuation, and notify top management."),
        ("Shift Incharge", "How do you manage unexpected high absenteeism at shift start?", "Cross-train critical operators to fill key safety-sensitive roles, adjust production line speeds, or request overtime extensions."),
        ("Shift Incharge", "What parameters must be reviewed in the daily shift report?", "Safety incidents, production target achievement vs variance, equipment downtime logs, and material raw consumption rates."),
        ("Shift Incharge", "What is the rule for authorizing a delayed maintenance job?", "Review the risk assessment, ensure a valid permit to work exists, and sign off as the area custodian."),
        ("Shift Incharge", "How do you enforce compliance with standard operating procedures (SOPs)?", "Conduct random on-the-spot tool-box talks and formal operator process audits during the shift."),

        # 13. Maintenance Engineer
        ("Maintenance Engineer", "What is the difference between preventive and breakdown maintenance?", "Preventive is scheduled work done to avoid failure; breakdown is unscheduled emergency repair executed after a machine stops."),
        ("Maintenance Engineer", "What does high oil analysis copper ppm indicate in a gearbox?", "It indicates severe wear and tear of bronze or brass components like bushings or thrust washers."),
        ("Maintenance Engineer", "What safety procedure is mandatory before working inside a slurry pump?", "Isolate mechanical drive (LOTO), close and lock suction/discharge valves, and drain the pump casing completely."),
        ("Maintenance Engineer", "What tool is used to monitor machine vibration trends?", "A digital vibration analyzer measuring velocity (mm/s) or acceleration to detect unbalance or loose parts."),
        ("Maintenance Engineer", "When should a hydraulic high-pressure hose be replaced?", "Immediately if there are signs of outer cover cracking, wire braid exposure, leaks, or localized blistering."),

        # 14. Forklift Operator
        ("Forklift Operator", "What is the speed limit for forklifts inside the plant sheds?", "The strict maximum speed limit is 8 km/h inside warehouses and production bays."),
        ("Forklift Operator", "How should a forklift be driven down a steep ramp with a load?", "Always drive in reverse with the load pointing uphill to prevent the forklift from tipping forward."),
        ("Forklift Operator", "What is the correct height of the forks while travelling?", "Keep the forks 4 to 6 inches (10-15 cm) off the ground, tilted slightly back to clear floor bumps safely."),
        ("Forklift Operator", "What should you do if a heavy load blocks your forward visibility?", "Drive the forklift in reverse, look over your shoulder, or use a designated spotter person to guide you."),
        ("Forklift Operator", "Where should the keys be kept when leaving a forklift parked?", "Turn off the engine, set the handbrake, lower forks to the floor, remove the key, and hand it to the supervisor."),

        # 15. Chemical Process Operator
        ("Chemical Process Operator", "What is the first action to take if acid splashes on skin?", "Immediately flush the area with copious amounts of clean running water for at least 15 to 20 minutes at an emergency eyewash station."),
        ("Chemical Process Operator", "Why is nitrogen purging used in chemical storage tanks?", "To displace oxygen and create an inert atmosphere, preventing fire or explosive chemical reactions."),
        ("Chemical Process Operator", "What does a sudden pressure drop across a chemical filter imply?", "It usually indicates a filter element rupture, bypass leak, or valve failure upstream."),
        ("Chemical Process Operator", "What specialized PPE is needed to handle liquid chlorine gas lines?", "A full-face positive pressure self-contained breathing apparatus (SCBA) and a chemical-resistant level A suit."),
        ("Chemical Process Operator", "How should chemical waste batches be logged?", "Document the exact pH, volume, chemical composition code, and transfer destination before moving it to treatment plants."),

        # 16. Boiler Operator
        ("Boiler Operator", "What is a boiler 'blowdown' and why is it performed?", "It is the removal of a portion of water from the boiler to reduce dissolved solids concentration and prevent scale buildup."),
        ("Flame/Water", "What is the most dangerous condition in a running boiler?", "A low-water condition. If water drops below the visible gauge glass, it can cause boiler tube overheating and explosive rupture."),
        ("Boiler Operator", "How often should safety valves on boilers be tested?", "Safety valves must be manually popped open or tested on a test bench once every month to prevent seizing."),
        ("Boiler Operator", "What does black smoke from a boiler stack indicate?", "Incomplete combustion caused by insufficient air supply, fuel overload, or poor fuel atomization."),
        ("Boiler Operator", "What is the function of an economizer in a boiler system?", "It recovers waste heat from the exhaust flue gases to preheat the incoming boiler feedwater, increasing efficiency."),

        # 17. Data Analyst
        ("Data Analyst", "How do you handle missing values in a daily plant sensor dataset?", "Depending on the variance, replace them using linear interpolation, forward fill for continuous data, or drop rows if data loss is under 1%."),
        ("Data Analyst", "What tool is used to create real-time operation dashboards?", "Power BI, Tableau, or custom python frameworks like Streamlit combined with Plotly graphs."),
        ("Data Analyst", "What is an anomaly detection model used for in production?", "To detect sudden spikes or shifts in machinery temperature/vibration that predict future equipment failure."),
        ("Data Analyst", "What database language is used to pull historical material records?", "Structured Query Language (SQL) using SELECT statements with conditional WHERE and JOIN clauses."),
        ("Data Analyst", "Why is data normalization important before running machine learning algorithms?", "It scales all numerical features to a uniform range (like 0 to 1), preventing variables with large scales from dominating the model."),

        # 18. Cybersecurity Analyst
        ("Cybersecurity Analyst", "What is the main goal of OT network segmentation?", "To isolate the industrial control systems (PLC/SCADA) from the standard corporate IT network, preventing malware spreads."),
        ("Cybersecurity Analyst", "How do you respond to a suspected ransomware attack on a workstation?", "Immediately disconnect the machine from the local network (unplug LAN/disable Wi-Fi) and report it to the security operation center."),
        ("Cybersecurity Analyst", "What is multi-factor authentication (MFA) and why enforce it?", "An identity verification method requiring two or more independent credentials, stopping 99% of automated credential theft attacks."),
        ("Cybersecurity Analyst", "What is the risk of using unauthorized USB drives on the shop floor?", "Introduction of malicious firmware or air-gap crossing malware (like Stuxnet) that can sabotage plant equipment."),
        ("Cybersecurity Analyst", "How often should industrial firewalls be audited?", "Firewall rule sets and access control lists (ACLs) must be reviewed and audited once every quarter."),

        # 19. Network Engineer
        ("Network Engineer", "What type of ethernet cable is best for hot shop floors?", "Industrial grade Shielded Twisted Pair (STP) Cat6 cables with ruggedized RJ45 jackets to block electromagnetic interference."),
        ("Network Engineer", "What is the purpose of a VLAN in plant networking?", "To logically separate different groups of devices (e.g., CCTV cameras vs PLC data) on the same physical network for security."),
        ("Network Engineer", "How do you diagnose a packet drop issue between two switches?", "Run a traceroute command, check interface error logs for CRC errors, and inspect physical fiber optic patch links."),
        ("Network Engineer", "What is network redundancy and why is it critical?", "Using dual configurations (like RSTP or ring topology) so if one network path fails, data automatically reroutes without stopping production."),
        ("Network Engineer", "What parameter determines wireless network health for autonomous AGVs?", "Signal-to-Noise Ratio (SNR) along with Received Signal Strength Indicator (RSSI) values across the plant layout."),

        # 20. Human Resource Executive
        ("Human Resource Executive", "What is the process for registering an employee for a mandatory retraining course?", "Identify gaps via the skill matrix portal, notify the employee and shift supervisor, and allocate a slot in the next L&D calendar batch."),
        ("Human Resource Executive", "How are employee grievances handled under Tata Steel guidelines?", "Grievances must be submitted to the HR partner, followed by an investigation committee review, and resolved within 14 working days."),
        ("Human Resource Executive", "What baseline matrix is checked during annual performance reviews?", "Course completion rates, safety compliance scores, core technical competency evaluations, and peer behavioral reviews."),
        ("Human Resource Executive", "What is the policy on maternity/paternity leave benefits?", "Tata Steel provides fully paid maternity leave of 26 weeks and paternity leave of 15 days as per corporate welfare standards."),
        ("Human Resource Executive", "How do you track training ROI for industrial labor?", "By comparing post-training production line quality scores and reduction in safety violations over a 6-month period."),

        # 21. Material Handling Operator
        ("Material Handling Operator", "What precaution must be taken before loading flatbed trailers with steel coils?", "Ensure the trailer bed is clean, chocks are locked into the anchor slots, and the trailer weight capacity is verified."),
        ("Material Handling Operator", "What is the maximum angle permissible for conveyor belt transport of raw iron ore?", "The angle of inclination should not exceed 18 degrees to prevent material roll-back or slippage."),
        ("Material Handling Operator", "What PPE is specific to manual handling of scrap steel?", "Heavy puncture-resistant Kevlar-lined leather gloves and meta-tarsal guard steel safety boots."),
        ("Material Handling Operator", "What should you do if an overhead magnetic lifter drops power?", "Clear the zone immediately, sound the horn, and do not enter the drop zone until the mechanical backup safety latches are checked."),
        ("Material Handling Operator", "How should damaged nylon lifting slings be handled?", "Cut the sling in half immediately so it cannot be reused, and throw it into the scrap bin."),

        # 22. Steel Plant Operator
        ("Steel Plant Operator", "What is the purpose of adding lime during the oxygen steelmaking process?", "Lime acts as a fluxing agent to react with impurities like silica and phosphorus, forming a floating slag layer."),
        ("Steel Plant Operator", "What is a caster breakout and how do you prevent it?", "A breakout is the rupture of the solidifying steel shell in a continuous casting machine. Prevented by strict mold level control and proper secondary cooling."),
        ("Steel Plant Operator", "What parameter controls steel grade hardness during secondary metallurgy?", "The precise injection of alloying elements like Manganese, Chromium, or Carbon inside the Ladle Furnace."),
        ("Steel Plant Operator", "What safety hazard is created by water moisture entering molten steel?", "A catastrophic steam explosion. All scrap metal and tools must be pre-heated and 100% dry before touching liquid steel."),
        ("Steel Plant Operator", "How is the thickness of a moving hot steel strip monitored?", "Using non-contact X-ray or isotope thickness measurement gauges positioned at the exit of the finishing mill stands."),

        # 23. Environmental Engineer
        ("Environmental Engineer", "What is the permissible PM10 limit for ambient air quality around steel plants?", "The standard permissible limit for PM10 is 100 micrograms per cubic meter for industrial zones over a 24-hour average."),
        ("Environmental Engineer", "How is waste pickle liquor (acidic waste) treated?", "It is sent to an Acid Regeneration Plant (ARP) to recover Hydrochloric acid, or neutralized using lime to precipitate iron sludge safely."),
        ("Environmental Engineer", "What is the purpose of a Continuous Emission Monitoring System (CEMS)?", "To track stack emissions of SO2, NOx, and CO2 in real-time and stream the data directly to the pollution control board servers."),
        ("Environmental Engineer", "How does a bagfilter house clean blast furnace gas?", "It passes the dirty gas through large fabric filter bags that catch micro-dust particles, allowing clean gas to flow out."),
        ("Environmental Engineer", "What is the target water recycling rate for Tata Steel plants?", "Tata Steel aims for a minimum of 98% water recycling rate through Zero Liquid Discharge (ZLD) treatment facilities."),

        # 24. Machine Operator
        ("Machine Operator", "What is the safety rule regarding loose clothing near a rotating lathe chuck?", "Loose clothing, ties, rings, and long un-tied hair are strictly forbidden to prevent entanglement hazards."),
        ("Machine Operator", "What tool should be used to clear metal chips from a cutting zone?", "Never use bare hands or rags; always use a dedicated long metal chip-hook brush while the machine is stopped."),
        ("Machine Operator", "What does a sudden chattering sound during a milling operation mean?", "It indicates excessive tool vibration caused by incorrect cutting speed, high feed rate, or a blunt cutting tool edge."),
        ("Machine Operator", "What is the function of cutting fluid/coolant?", "To cool the cutting tool edge, lubricate the chip slide zone, and wash away scrap chips from the cutting interface."),
        ("Machine Operator", "When must an E-stop switch be reset?", "Only after the hazard has been completely removed, the machine is inspected, and it is safe to resume work."),

        # 25. Thermal Power Technician
        ("Thermal Power Technician", "What safety routine is executed before entering a condenser water box?", "Isolate inlet/discharge valves (LOTO), vent internal pressure, test for confined space oxygen levels, and secure a standby buddy."),
        ("Thermal Power Technician", "What is steam turbine 'rolling'?", "The process of slowly admitting high-temperature steam into the turbine casing to heat the rotor uniformly and avoid thermal bending."),
        ("Thermal Power Technician", "What does high dissolved oxygen in boiler feedwater cause?", "Severe pitting corrosion on the internal metallic walls of high-pressure boiler tubes."),
        ("Thermal Power Technician", "What is the function of an electrostatic precipitator (ESP)?", "It uses high-voltage electric fields to charge and collect fly ash dust from flue gases before they escape the chimney stack."),
        ("Thermal Power Technician", "What parameter requires immediate trip action on a steam turbine?", "Vibration crossing the critical high threshold or a sudden total drop in lubrication oil header pressure.")
    ]

    cursor.executemany("INSERT INTO fixed_faqs (role, question, answer) VALUES (?, ?, ?)", all_roles_data)
    conn.commit()
    print(f"Success! Loaded {len(all_roles_data)} fixed QAs for all 25 departments inside 'tatasteel_ld.db'.")
    conn.close()

if __name__ == "__main__":
    init_database()