# Organization-User Relationship Guide

这个指南展示了如何使用Organization和User之间的多对多关系，支持用户在组织中的不同角色管理。

## 核心概念

### 1. 多对多关系
- 一个Organization可以有多个Users
- 一个User可以属于多个Organizations
- 通过`UserOrganization`中间表管理关系和角色

### 2. 用户角色
```python
class OrganizationRole(str, enum.Enum):
    OWNER = "owner"      # 拥有者，最高权限
    ADMIN = "admin"      # 管理员，管理权限
    MANAGER = "manager"  # 经理，部分管理权限
    MEMBER = "member"    # 普通成员
    GUEST = "guest"      # 访客，只读权限
```

## 使用示例

### 1. 创建组织并添加用户

```python
from agir_db.models import Organization, User, UserOrganization, OrganizationRole
from agir_db.schemas import OrganizationCreate, UserOrganizationCreate

# 创建组织
org_data = OrganizationCreate(
    name="Tech Company",
    organization_type="company",
    city="Beijing",
    country="China"
)

# 假设已有组织和用户实例
organization = Organization(**org_data.dict())
user1 = User(email="user1@example.com")
user2 = User(email="user2@example.com")

# 添加用户到组织
membership1 = UserOrganization(
    user_id=user1.id,
    organization_id=organization.id,
    role=OrganizationRole.ADMIN,
    added_by=current_user.id  # 谁添加了这个用户
)

membership2 = UserOrganization(
    user_id=user2.id,
    organization_id=organization.id,
    role=OrganizationRole.MEMBER
)
```

### 2. 批量添加用户

```python
from agir_db.schemas import OrganizationMembershipRequest

# 批量添加用户
membership_request = OrganizationMembershipRequest(
    user_ids=[user1.id, user2.id, user3.id],
    role=OrganizationRole.MEMBER
)

# 在API中处理
for user_id in membership_request.user_ids:
    membership = UserOrganization(
        user_id=user_id,
        organization_id=organization.id,
        role=membership_request.role,
        added_by=current_user.id
    )
    db.add(membership)
```

### 3. 查询组织成员

```python
# 获取组织的所有活跃用户
active_users = organization.get_active_users()

# 获取特定角色的用户
admins = organization.get_users_by_role(OrganizationRole.ADMIN)
members = organization.get_users_by_role(OrganizationRole.MEMBER)

# 检查用户是否在组织中
is_member = organization.has_user(user.id)

# 获取用户在组织中的角色
user_role = organization.get_user_role(user.id)
```

### 4. 查询用户的组织

```python
# 通过关系查询
user_organizations = user.organizations  # 返回所有用户所属的组织
user_memberships = user.organization_memberships  # 返回详细的成员关系

# 获取用户在特定组织中的角色
for membership in user.organization_memberships:
    if membership.organization_id == organization.id:
        print(f"用户在{membership.organization.name}中的角色是: {membership.role}")
```

### 5. 角色管理

```python
from agir_db.schemas import RoleChangeRequest

# 更改用户角色
role_change = RoleChangeRequest(
    user_id=user.id,
    new_role=OrganizationRole.MANAGER
)

# 在数据库中更新
membership = db.query(UserOrganization).filter(
    UserOrganization.user_id == role_change.user_id,
    UserOrganization.organization_id == organization.id
).first()

if membership:
    membership.role = role_change.new_role
    membership.updated_at = datetime.utcnow()
    db.commit()
```

### 6. 组织邀请

```python
from agir_db.schemas import OrganizationInvitation

# 创建邀请
invitation = OrganizationInvitation(
    organization_id=organization.id,
    user_email="newuser@example.com",
    role=OrganizationRole.MEMBER,
    message="欢迎加入我们的团队！"
)

# 处理邀请逻辑
# 1. 查找或创建用户
# 2. 创建UserOrganization记录
# 3. 发送邀请邮件
```

### 7. 层级组织中的用户管理

```python
# 在企业层级结构中管理用户
company = Organization(name="Tech Corp", organization_type="company")
subsidiary = Organization(name="AI Division", parent_id=company.id)
department = Organization(name="Research Team", parent_id=subsidiary.id)

# 用户可以在不同层级中有不同角色
# CEO在公司层面是OWNER
ceo_membership = UserOrganization(
    user_id=ceo.id,
    organization_id=company.id,
    role=OrganizationRole.OWNER
)

# 同一个用户在子公司是ADMIN
ceo_subsidiary = UserOrganization(
    user_id=ceo.id,
    organization_id=subsidiary.id,
    role=OrganizationRole.ADMIN
)

# 研究员在部门是MEMBER
researcher_membership = UserOrganization(
    user_id=researcher.id,
    organization_id=department.id,
    role=OrganizationRole.MEMBER
)
```

## API Schema 使用

### 1. 获取组织成员列表

```python
from agir_db.schemas import OrganizationMembersList

# API返回格式
members_response = OrganizationMembersList(
    members=[
        UserOrganizationDetail(
            id=membership.id,
            user_id=membership.user_id,
            organization_id=membership.organization_id,
            role=membership.role,
            joined_at=membership.joined_at,
            user=UserBrief(
                id=membership.user.id,
                email=membership.user.email,
                first_name=membership.user.first_name,
                is_active=membership.user.is_active
            )
        )
        for membership in organization.user_memberships
    ],
    total=len(organization.user_memberships),
    page=1,
    page_size=10,
    has_next=False,
    has_prev=False
)
```

### 2. 获取用户的组织列表

```python
from agir_db.schemas import UserOrganizationsList

user_orgs_response = UserOrganizationsList(
    organizations=[
        UserOrganizationDetail(
            id=membership.id,
            user_id=membership.user_id,
            organization_id=membership.organization_id,
            role=membership.role,
            joined_at=membership.joined_at,
            organization=OrganizationBrief(
                id=membership.organization.id,
                name=membership.organization.name,
                organization_type=membership.organization.organization_type,
                is_active=membership.organization.is_active
            )
        )
        for membership in user.organization_memberships
    ],
    total=len(user.organization_memberships),
    page=1,
    page_size=10,
    has_next=False,
    has_prev=False
)
```

## 数据库约束

1. **唯一性约束**: 每个用户在同一个组织中只能有一个活跃的成员关系
2. **外键约束**: 确保用户和组织都存在
3. **级联删除**: 当组织被删除时，相关的成员关系也会被删除

## 最佳实践

1. **权限检查**: 在执行操作前检查用户权限
2. **软删除**: 使用`is_active`字段而不是直接删除记录
3. **审计跟踪**: 记录谁添加了用户到组织(`added_by`字段)
4. **批量操作**: 对于大量用户操作，使用批量API
5. **缓存**: 对于频繁查询的组织-用户关系，考虑使用缓存

## 示例API端点

```python
# FastAPI 路由示例
@app.post("/organizations/{org_id}/members")
async def add_members(
    org_id: UUID,
    request: OrganizationMembershipRequest,
    current_user: User = Depends(get_current_user)
):
    # 添加成员逻辑
    pass

@app.get("/organizations/{org_id}/members")
async def get_members(org_id: UUID) -> OrganizationMembersList:
    # 获取成员列表逻辑
    pass

@app.put("/organizations/{org_id}/members/{user_id}/role")
async def change_user_role(
    org_id: UUID,
    user_id: UUID,
    request: RoleChangeRequest
):
    # 更改角色逻辑
    pass
```

这个系统提供了灵活且强大的组织-用户关系管理，支持复杂的企业结构和权限系统。 