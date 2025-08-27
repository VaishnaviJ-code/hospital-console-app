from services.LabTechnicianLib import LabTechnicianLib

def test_id_generation():
    """Test test ID generation"""
    print("Testing Test ID Generation...")
    
    # Generate multiple IDs to see the sequence
    for i in range(5):
        test_id = LabTechnicianLib.generate_test_id()
        print(f"Generated Test ID {i+1}: {test_id}")

if __name__ == "__main__":
    test_id_generation()
