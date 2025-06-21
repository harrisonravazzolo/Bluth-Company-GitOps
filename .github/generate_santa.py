#!/usr/bin/env python3
"""
Google Santa MobileConfig Generator
Reads a template file and replaces the StaticRules placeholder with rules from JSON
"""

import json
import argparse
import sys

def generate_static_rules_xml(rules, indent_level=7):
    """Generate the StaticRules XML section from JSON rules"""
    
    # Base indentation (7 tabs to match the template structure)
    base_indent = '\t' * indent_level
    rule_indent = '\t' * (indent_level + 1)
    key_indent = '\t' * (indent_level + 2)
    
    xml_parts = []
    
    for rule in rules:
        # Start rule dict
        xml_parts.append(f"{rule_indent}<dict>")
        
        # Add comment if present
        if 'comment' in rule and rule['comment']:
            xml_parts.append(f"{key_indent}<!-- {rule['comment']} -->")
        
        # Add identifier
        xml_parts.append(f"{key_indent}<key>identifier</key>")
        xml_parts.append(f"{key_indent}<string>{rule['identifier']}</string>")
        
        # Add policy
        xml_parts.append(f"{key_indent}<key>policy</key>")
        xml_parts.append(f"{key_indent}<string>{rule['policy']}</string>")
        
        # Add rule_type
        xml_parts.append(f"{key_indent}<key>rule_type</key>")
        xml_parts.append(f"{key_indent}<string>{rule['rule_type']}</string>")
        
        # End rule dict
        xml_parts.append(f"{rule_indent}</dict>")
    
    return '\n'.join(xml_parts)

def main():
    parser = argparse.ArgumentParser(description='Generate Google Santa .mobileconfig from template and JSON rules')
    parser.add_argument('--template', required=True, help='Template .mobileconfig file')
    parser.add_argument('--rules', required=True, help='JSON rules file')
    parser.add_argument('--output', '-o', help='Output .mobileconfig file (default: santa_profile.mobileconfig)')
    
    args = parser.parse_args()
    
    # Default output filename
    output_file = args.output if args.output else 'santa_profile.mobileconfig'
    
    try:
        # Load template file
        with open(args.template, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Load JSON rules
        with open(args.rules, 'r') as f:
            rules_data = json.load(f)
        
        # Handle both single rule and array of rules
        if isinstance(rules_data, dict):
            rules = [rules_data]  # Single rule
        elif isinstance(rules_data, list):
            rules = rules_data     # Array of rules
        else:
            print("❌ Error: JSON must be either a single rule object or array of rules")
            sys.exit(1)
        
        # Validate rules
        for i, rule in enumerate(rules):
            required_fields = ['identifier', 'policy', 'rule_type']
            for field in required_fields:
                if field not in rule:
                    print(f"❌ Error: Rule {i+1} missing required field '{field}'")
                    sys.exit(1)
        
        # Generate StaticRules XML
        static_rules_xml = generate_static_rules_xml(rules)
        
        # Replace placeholder in template
        placeholder = "static_rules from rules.json go here"
        if placeholder not in template_content:
            print(f"❌ Error: Template file does not contain placeholder: '{placeholder}'")
            sys.exit(1)
        
        # Replace the placeholder with generated rules
        final_content = template_content.replace(placeholder, static_rules_xml)
        
        # Write the final file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✅ Successfully generated {output_file}")
        print(f"📊 Added {len(rules)} rules to StaticRules section")
        
        # Show rule summary
        allowlist_count = len([r for r in rules if r['policy'].upper() == 'ALLOWLIST'])
        blocklist_count = len([r for r in rules if r['policy'].upper() == 'BLOCKLIST'])
        print(f"   - {allowlist_count} ALLOWLIST rules")
        print(f"   - {blocklist_count} BLOCKLIST rules")
        
        print(f"\n📋 Rules added:")
        for i, rule in enumerate(rules, 1):
            comment = rule.get('comment', 'No comment')
            print(f"   {i}. {rule['policy']} {rule['rule_type']}: {rule['identifier']}")
            if comment != 'No comment':
                print(f"      Comment: {comment}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found: {e.filename}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{args.rules}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()