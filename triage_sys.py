import networkx as nx
import heapq
import pandas
import random


class Patient:
    def __init__(self, patient_id):
        self.id = patient_id
        self.severity = random.randint(1, 10)  # Higher means more critical
        self.heart_rate = random.randint(60, 150)  # Normal: 60-100
        self.oxygen_level = random.randint(85, 100)  # Normal: 95-100
        self.symptom_severity = random.randint(
            1, 10)  # Higher = worse symptoms
        self.anxiety_index = random.uniform(
            0, 1)  # Higher = more anxiety-prone
        self.pain_exaggeration = random.uniform(
            0, 1)  # Higher = possible drug-seeker

    def update_condition(self):
        """Simulate real-time worsening conditions"""
        if random.random() < 0.3:  # 30% chance condition worsens
            self.severity += random.randint(1, 3)
            self.heart_rate += random.randint(5, 15)
            self.oxygen_level -= random.randint(1, 5)
            self.symptom_severity += random.randint(1, 3)

            # Anxiety patients may worsen unpredictably
            if self.anxiety_index > 0.7 and random.random() < 0.5:
                self.heart_rate += random.randint(10, 20)
                self.symptom_severity += random.randint(2, 4)


def detect_drug_seeking(patient):
    """Identify possible drug-seeking behavior"""
    if patient.pain_exaggeration > 0.7 and patient.symptom_severity > 7 and patient.severity < 5:
        return True  # High symptoms, low actual distress
    return False


def detect_high_anxiety(patient):
    """Identify patients at risk of anxiety-induced worsening"""
    if patient.anxiety_index > 0.7 and patient.heart_rate > 120:
        return True  # High anxiety & elevated heart rate
    return False


def build_patient_graph(patients):
    G = nx.DiGraph()

    for p in patients:
        G.add_node(p.id, severity=p.severity, symptoms=p.symptom_severity)

    # Add edges based on symptom similarity or severity
    for i, p1 in enumerate(patients):
        for j, p2 in enumerate(patients):
            if i != j:  # No self-loops
                severity_diff = abs(p1.severity - p2.severity)
                symptom_diff = abs(p1.symptom_severity - p2.symptom_severity)
                # Lower difference = stronger link
                weight = 1 / (1 + severity_diff + symptom_diff)

                if weight > 0.2:  # Only add significant connections
                    G.add_edge(p1.id, p2.id, weight=weight)

    return G


def compute_patient_pagerank(G):
    pagerank_scores = nx.pagerank(
        G, alpha=0.85, weight='weight')  # Standard damping factor
    return pagerank_scores


def prioritize_patients(patients, pagerank_scores):
    priority_queue = []

    for p in patients:
        # Higher PageRank score = Higher priority
        heapq.heappush(priority_queue, (-pagerank_scores[p.id], p))

    return priority_queue


def process_patients(priority_queue):
    while priority_queue:
        _, patient = heapq.heappop(priority_queue)  # Get most critical patient
        drug_seeker = detect_drug_seeking(patient)
        anxiety_risk = detect_high_anxiety(patient)

        status = f"🚑 Treating Patient {patient.id} (Severity: {patient.severity})"

        if drug_seeker:
            status += " ⚠️ Possible Drug-Seeker"
        if anxiety_risk:
            status += " 🔴 High Anxiety Risk"

        print(status)


# Step 1: Create patients
num_patients = 10
patients = [Patient(i) for i in range(num_patients)]

# Step 2: Build patient graph
patient_graph = build_patient_graph(patients)

# Step 3: Compute PageRank scores
pagerank_scores = compute_patient_pagerank(patient_graph)

# Step 4: Prioritize patients
priority_queue = prioritize_patients(patients, pagerank_scores)

# Step 5: Process patients in order of severity
process_patients(priority_queue)
