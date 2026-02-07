#!/usr/bin/env python3
"""
Test script to demonstrate Chico Chihuahua animations
"""

import time
import animations

print("=" * 80)
print("CHICO CHIHUAHUA CLI - ANIMATION SHOWCASE")
print("Testing the 'Small Dog, Big Power' theme")
print("=" * 80)
print()

# Test 1: Banner
print("TEST 1: Show Banner")
print("-" * 80)
animations.show_banner()
time.sleep(1)

# Test 2: ASCII Art Gallery
print("\n\nTEST 2: ASCII Art Gallery")
print("-" * 80)
poses = [
    ("sitting", "Chico is ready to work!"),
    ("coding", "Coding incredible worlds..."),
    ("launching", "Launching powerful integrations..."),
    ("searching", "Searching through vast databases..."),
    ("power", "Feel the Chihuahua power!"),
    ("success", "Mission accomplished!")
]

for pose, message in poses:
    animations.show_chico_art(pose, message)
    time.sleep(0.8)
    print()

# Test 3: Success Animation
print("\n\nTEST 3: Success Animation")
print("-" * 80)
animations.success_animation("API Configuration Complete!")
time.sleep(1)

# Test 4: Config Success
print("\n\nTEST 4: Configuration Success Animation")
print("-" * 80)
animations.config_success_animation()
time.sleep(1)

# Test 5: Provider Switch
print("\n\nTEST 5: Provider Switch Animation")
print("-" * 80)
animations.provider_switch_animation("OpenRouter", "Ollama Cloud")
time.sleep(1)

# Test 6: Model Listing
print("\n\nTEST 6: Model Listing Animation")
print("-" * 80)
animations.model_listing_animation()
time.sleep(1)

# Test 7: Interactive Start
print("\n\nTEST 7: Interactive Mode Start")
print("-" * 80)
animations.interactive_start_animation()
time.sleep(1)

# Test 8: Motivational Messages
print("\n\nTEST 8: Motivational Messages")
print("-" * 80)
for i in range(3):
    animations.show_motivational_message()
    time.sleep(0.5)

# Test 9: Big Feat Celebrations
print("\n\nTEST 9: Big Feat Celebrations")
print("-" * 80)
feats = [
    "Coded the World",
    "Launched Integration",
    "Powered Search Engine",
    "Mastered AI"
]
for feat in feats:
    animations.big_feat_celebration(feat)
    time.sleep(0.8)

# Test 10: Quick Functions
print("\n\nTEST 10: Quick Animation Functions")
print("-" * 80)
animations.quick_loading("Loading data...")
time.sleep(0.5)
animations.quick_success("Data loaded successfully!")
time.sleep(0.5)

print("\n\n" + "=" * 80)
print("ALL ANIMATIONS TESTED SUCCESSFULLY!")
print("Tiny Chihuahua with BIG presentation power! 🐕⚡")
print("=" * 80)
