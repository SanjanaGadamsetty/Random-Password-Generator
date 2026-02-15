import random
import string
from datetime import datetime

def get_valid_input(prompt, min_value=None, max_value=None, input_type=int):
    """Get valid input from user with error handling"""
    while True:
        try:
            value = input_type(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid value.")

def get_yes_no_input(prompt):
    """Get yes/no input from user - O(1) complexity"""
    while True:
        value = input(prompt).lower()
        if value in {'y', 'yes'}:
            return True
        elif value in {'n', 'no'}:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def get_character_preferences():
    """Get user preferences for character types - optimized"""
    print("\n=== Character Type Preferences ===")
    
    # Use dictionary for faster lookups
    letter_options = {'1': 'upper', '2': 'lower', '3': 'mixed'}
    
    while True:
        include_letters = get_yes_no_input("Include letters (y/n)? ")
        
        letter_case = None
        if include_letters:
            while True:
                print("\nLetter case options:")
                print("1. Uppercase only")
                print("2. Lowercase only")
                print("3. Mixed case")
                choice = input("Select letter case (1-3): ").strip()
                
                if choice in letter_options:
                    letter_case = letter_options[choice]
                    break
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        include_digits = get_yes_no_input("Include digits (y/n)? ")
        include_symbols = get_yes_no_input("Include symbols (y/n)? ")
        
        # Count selected types without list creation
        selected_count = (1 if include_letters else 0) + \
                        (1 if include_digits else 0) + \
                        (1 if include_symbols else 0)
        
        if selected_count < 2:
            print("\n" + "!" * 50)
            print("ERROR: You must select at least TWO character types!")
            print("!" * 50 + "\n")
            print("Let's try again...")
            continue
        
        if include_letters and letter_case is None:
            letter_case = 'mixed'
        
        return {
            'include_letters': include_letters,
            'letter_case': letter_case,
            'include_digits': include_digits,
            'include_symbols': include_symbols
        }

def validate_date(dob_str):
    """Validate date format - optimized with single try-catch"""
    current_date = datetime.now()
    
    # Common date formats
    for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
        try:
            date_obj = datetime.strptime(dob_str, fmt)
            
            if date_obj > current_date:
                return None, "Date cannot be in the future."
            
            return date_obj.strftime('%d%m%Y'), None
            
        except ValueError:
            continue
    
    return None, "Invalid date format. Use DD/MM/YYYY or DD-MM-YYYY."

def get_base_word_selection(preferences):
    """Get base word selection - optimized with precomputed messages"""
    print("\n=== Base Word Selection ===")
    print("1. Your Name")
    print("2. Your Date of Birth (DOB)")
    print("3. Any other custom word/phrase")
    print("4. A mixture of these")
    print("5. No base word – Generate a fully random password")
    
    warnings = {
        2: ("WARNING: You selected 'NO' for digits!\n"
            "Option 2 (DOB) will only contain digits.\n"
            "This might not generate a valid password."),
        1: ("WARNING: You selected 'NO' for letters!\n"
            "Option 1 (Name) will only contain letters.\n"
            "This might not generate a valid password."),
        3: ("NOTE: You selected 'NO' for letters.\n"
            "Custom words typically contain letters.\n"
            "Your custom word might be modified.")
    }
    
    while True:
        try:
            choice = int(input("Select an option (1-5): "))
            if not 1 <= choice <= 5:
                print("Please enter a number between 1 and 5.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice in warnings:
            if (choice == 2 and not preferences['include_digits']) or \
               (choice == 1 and not preferences['include_letters']) or \
               (choice == 3 and not preferences['include_letters']):
                print("\n" + "!" * 50)
                print(warnings[choice])
                print("!" * 50)
                
                if not get_yes_no_input("\nContinue anyway? (y/n): "):
                    continue
        
        break
    
    base_data = {}
    
    if choice in (1, 4):
        name = input("Enter your name: ").strip()
        if name:
            base_data['name'] = name
    
    if choice in (2, 4):
        while True:
            dob = input("Enter your Date of Birth (DD/MM/YYYY or DD-MM-YYYY): ").strip()
            formatted_date, error = validate_date(dob)
            
            if error:
                print(f"Error: {error}")
                if not get_yes_no_input("Try again? (y/n): "):
                    break
                continue
            
            if formatted_date:
                base_data['dob'] = formatted_date
                break
    
    if choice in (3, 4):
        custom_word = input("Enter a custom word or phrase: ").strip()
        if custom_word:
            base_data['custom'] = custom_word
    
    return choice, base_data

def create_character_pool(preferences):
    """Create character pool - optimized string concatenation"""
    # Precomputed character sets
    char_sets = {
        'upper': string.ascii_uppercase,
        'lower': string.ascii_lowercase,
        'mixed': string.ascii_letters,
        'digits': string.digits,
        'symbols': string.punctuation
    }
    
    pool_parts = []
    
    if preferences['include_letters']:
        pool_parts.append(char_sets[preferences['letter_case']])
    
    if preferences['include_digits']:
        pool_parts.append(char_sets['digits'])
    
    if preferences['include_symbols']:
        pool_parts.append(char_sets['symbols'])
    
    return ''.join(pool_parts)  # More efficient than += in loop

def create_filtered_base_string(base_data, preferences):
    """Create filtered base string - optimized with list comprehension"""
    base_parts = []
    
    if 'name' in base_data and preferences['include_letters']:
        name = base_data['name']
        if preferences['letter_case'] == 'upper':
            name = name.upper()
        elif preferences['letter_case'] == 'lower':
            name = name.lower()
        base_parts.append(name)
    
    if 'dob' in base_data and preferences['include_digits']:
        base_parts.append(base_data['dob'])
    
    if 'custom' in base_data:
        custom = base_data['custom']
        # Use list comprehension for filtering
        filtered = []
        for char in custom:
            if preferences['include_letters'] and char.isalpha():
                if preferences['letter_case'] == 'upper':
                    filtered.append(char.upper())
                elif preferences['letter_case'] == 'lower':
                    filtered.append(char.lower())
                else:
                    filtered.append(char)
            elif preferences['include_digits'] and char.isdigit():
                filtered.append(char)
            elif preferences['include_symbols'] and char in string.punctuation:
                filtered.append(char)
        
        if filtered:
            base_parts.append(''.join(filtered))
    
    return ''.join(base_parts)

def generate_password_optimized(length, character_pool, base_choice, base_data, preferences):
    """Generate password - optimized with single shuffle"""
    if base_choice == 5 or not base_data:
        # Generate random password directly
        return ''.join(random.choices(character_pool, k=length))
    
    # Get filtered base string
    base_string = create_filtered_base_string(base_data, preferences)
    
    if not base_string:
        print("\nNote: Base word filtered out. Generating random password.")
        return ''.join(random.choices(character_pool, k=length))
    
    # Limit base string length efficiently
    max_base_len = min(len(base_string), int(length * 0.6))
    if len(base_string) > max_base_len:
        base_string = base_string[:max_base_len]
    
    # Calculate remaining length
    remaining = length - len(base_string)
    
    # Generate all characters at once
    random_chars = ''.join(random.choices(character_pool, k=remaining))
    
    # Combine and shuffle once
    combined = list(base_string + random_chars)
    random.shuffle(combined)
    
    return ''.join(combined)

def validate_password_efficient(password, preferences, length):
    """Validate password - optimized single pass"""
    if len(password) != length or len(password) < 8:
        return False, f"Invalid length: {len(password)} (required: {length}, min: 8)"
    
    # Single pass through password
    has_upper = has_lower = has_digit = has_symbol = False
    type_count = 0
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in string.punctuation:
            has_symbol = True
    
    # Count types without extra operations
    type_count = (1 if has_upper or has_lower else 0) + \
                 (1 if has_digit else 0) + \
                 (1 if has_symbol else 0)
    
    if type_count < 2:
        return False, f"Only {type_count} character type(s). Need at least 2."
    
    # Check preferences
    if preferences['include_letters']:
        if preferences['letter_case'] == 'mixed' and not (has_upper and has_lower):
            return False, "Need both uppercase and lowercase"
        elif preferences['letter_case'] == 'upper' and not has_upper:
            return False, "Need uppercase"
        elif preferences['letter_case'] == 'lower' and not has_lower:
            return False, "Need lowercase"
    
    if preferences['include_digits'] and not has_digit:
        return False, "Need digits"
    
    if preferences['include_symbols'] and not has_symbol:
        return False, "Need symbols"
    
    return True, "Valid"

def generate_password_with_retry(length, preferences, base_choice, base_data):
    """Generate password with retry - optimized"""
    character_pool = create_character_pool(preferences)
    
    if not character_pool:
        return None, "No character types selected"
    
    max_attempts = 50  # Reduced from 100
    best_password = None
    best_score = -1
    
    for attempt in range(max_attempts):
        password = generate_password_optimized(length, character_pool, base_choice, base_data, preferences)
        is_valid, message = validate_password_efficient(password, preferences, length)
        
        if is_valid:
            return password, message
        
        # Keep track of best attempt
        # Score based on length and type count
        score = len(password)
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
            
        if score > best_score:
            best_score = score
            best_password = password
    
    # Return best attempt if no perfect match
    return best_password, "Generated best possible password"

def display_results(password, length, preferences, validation_msg):
    """Display results - optimized"""
    print(f"\nGenerated Password: {password}")
    print(f"Length: {len(password)} (requested: {length})")
    
    if "best possible" in validation_msg.lower():
        print(f"\n⚠ Note: {validation_msg}")
    
    # Count efficiently using sum() with generator
    counts = {
        'upper': sum(1 for c in password if c.isupper()),
        'lower': sum(1 for c in password if c.islower()),
        'digit': sum(1 for c in password if c.isdigit()),
        'symbol': sum(1 for c in password if c in string.punctuation)
    }
    
    print("\nCharacter breakdown:")
    for type_name, count in counts.items():
        if count > 0:
            print(f"  {type_name.title()}: {count}")

def main_optimized():
    """Main function - optimized"""
    print("=" * 50)
    print("OPTIMIZED PASSWORD GENERATOR")
    print("=" * 50)
    
    while True:
        print("\n1. Generate password")
        print("2. Exit")
        
        choice = input("Select (1-2): ").strip()
        if choice == '2':
            print("\nGoodbye!")
            break
        elif choice != '1':
            continue
        
        # Get inputs
        length = get_valid_input("\nPassword length (min 8): ", 8)
        preferences = get_character_preferences()
        base_choice, base_data = get_base_word_selection(preferences)
        
        # Generate password
        print("\n" + "=" * 50)
        print("GENERATING...")
        
        password, message = generate_password_with_retry(length, preferences, base_choice, base_data)
        
        if password:
            display_results(password, length, preferences, message)
        
        # Continue?
        if not get_yes_no_input("\nGenerate another? (y/n): "):
            print("\nThe Password is Generated Successfully..!\nGood Bye!")
            break

if __name__ == "__main__":
    main_optimized()