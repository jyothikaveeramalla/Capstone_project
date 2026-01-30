# Artisan Team Feature Guide

## Overview

The Team feature allows multiple artisans to work together and share products. When products are added by any team member, they are automatically visible to all team members.

## How It Works

### 1. Creating a Team

Artisans can create a team to collaborate with other artisans:

- Go to: `Artisan Dashboard > Create Team` or navigate to `/artisans/teams/create/`
- Enter team name and description
- The creator automatically becomes the team admin

### 2. Adding Team Members

Team admins can add other artisans to their team:

- Go to: `Team Dashboard > Add Member`
- Enter the email address of the artisan you want to add
- The artisan must have an active artisan profile
- Select their role (Admin or Member)

### 3. Product Visibility for Teams

**Before:** Each artisan could only see their own products
**After:** 
- Products created by any team member are visible to all team members
- Products are automatically assigned to the team when created
- Team members can edit/delete any team product (if they have permission)
- The "My Products" view shows both individual and team products

## How Products Work in Teams

### Product Creation

When an artisan creates a product:
1. If they are part of a team, the product is automatically assigned to that team
2. The artisan's profile is still recorded as the creator
3. All team members can see and manage the product

### Product Ownership

Products can be owned by:
- **Individual Artisan**: Created by an artisan not in a team
- **Team**: Created by a team member or assigned to a team

### Accessing Team Products

Team members can:
- View all products created by their team
- Edit products created by team members
- Delete products created by team members
- See team-based products in their "My Products" dashboard

## Models

### ArtisanTeam
```
- name: Team name
- description: Team description
- owner: The user who created the team
- created_at: Creation timestamp
- updated_at: Last update timestamp
```

### ArtisanTeamMember
```
- team: Reference to the team
- user: Team member user
- role: 'admin' or 'member'
- joined_at: When user joined the team
```

### ArtisanProfile
```
- team: (NEW) Reference to team if artisan is part of one
```

### Product
```
- artisan: Original artisan creator
- team: (NEW) Team that owns the product (optional)
```

## Database Queries

### Get all products for a team member:
```python
from artisans.models import ArtisanProfile
from products.models import Product

artisan = ArtisanProfile.objects.get(user=request.user)

# Get individual products
individual_products = Product.objects.filter(artisan=artisan)

# Get team products
if artisan.team:
    team_products = Product.objects.filter(team=artisan.team)
    all_products = individual_products.union(team_products)
else:
    all_products = individual_products
```

### Get team members:
```python
from artisans.models import ArtisanTeam

team = ArtisanTeam.objects.get(id=team_id)
members = team.get_members()  # Returns all team members

# Or using direct access:
members = team.members.all()
```

## URLs

### Team Management Routes

```
/artisans/teams/my/                           - View all my teams
/artisans/teams/create/                       - Create a new team
/artisans/teams/<team_id>/                    - Team dashboard
/artisans/teams/<team_id>/add-member/         - Add team member
/artisans/teams/<team_id>/remove-member/<member_id>/  - Remove team member
/artisans/teams/<team_id>/leave/              - Leave a team
```

### Product Management Routes

```
/products/manage/my/                          - My products (individual + team)
/products/manage/add/                         - Add new product
/products/manage/<product_id>/edit/           - Edit product
/products/manage/<product_id>/delete/         - Delete product
```

## Permission Rules

### Creating/Managing Teams
- Only artisans can create teams
- Only team admins can add/remove members

### Managing Products
- Artisans can edit/delete their own products
- Team members can edit/delete team products
- Staff can edit/delete any product

### Leaving Teams
- Regular members can leave anytime
- Team owner cannot leave without reassigning ownership

## Admin Interface

### Team Management
Admins can manage teams in Django admin:
- View all teams and members
- Add/remove team members
- See team statistics

### Product Admin Updates
Products now show:
- Owner (artisan or team name)
- Team assignment
- Filter by team

## Migration Details

Two migrations were created:

1. **artisans** app:
   - Created `ArtisanTeam` model
   - Created `ArtisanTeamMember` model
   - Added `team` field to `ArtisanProfile`

2. **products** app:
   - Added `team` field to `Product`
   - Added index for team + status filtering

Both migrations are backward compatible. Existing artisans can continue working individually without creating a team.

## Testing the Feature

### Step 1: Create a Team
```
1. Sign up/Login as Artisan A
2. Go to Create Team
3. Create team "Artisan Workshop"
```

### Step 2: Add Team Member
```
1. As Artisan A, go to Team Dashboard
2. Click "Add Member"
3. Enter Artisan B's email
4. Artisan B is now part of the team
```

### Step 3: Test Product Visibility
```
1. Login as Artisan A
2. Add a product "Product 1"
3. Logout and Login as Artisan B
4. Go to "My Products"
5. You should see "Product 1" created by Artisan A
6. Both can edit/delete the product
```

## Troubleshooting

### "Email not found" error
- Make sure the user exists in the system
- User must have an artisan profile

### Cannot add member
- Check if user is already in the team
- Verify user is an artisan (has artisan profile)

### Products not visible to team members
- Make sure artisan's profile has team assigned
- Check product.team field in admin
- Verify team membership in ArtisanTeamMember table

## Future Enhancements

Potential improvements:
- Assign roles with different permissions
- Revenue sharing between team members
- Team statistics and analytics
- Invite system with email notifications
- Team image/branding
- Team performance metrics
